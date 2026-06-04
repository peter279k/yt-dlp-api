import os
from pathlib import Path

import yt_dlp
from celery import Celery

DOWNLOAD_DIR = Path('/app/downloads/')
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

celery = Celery(
    "worker",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="rpc://",
)

@celery.task
def download_video_task(url: str, job_id: str) -> str:
    filepath = os.path.join(DOWNLOAD_DIR, f"{job_id}.mp4")
    ydl_opts = {
        "outtmpl": filepath,
        "format": "best",
        'js_runtimes': {
            'deno': {
                'path': '/home/appuser/.deno/bin/deno'
            },
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        log_path = os.path.join(DOWNLOAD_DIR, f"{job_id}.log")
        with open(log_path, 'w') as f:
            f.write(f'{str(e)}\n')

    return filepath
