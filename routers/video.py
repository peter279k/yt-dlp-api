import os
import uuid
import yt_dlp
from urllib.parse import urlparse

from fastapi import HTTPException, Query
from fastapi.responses import FileResponse

from app.workers.worker import DOWNLOAD_DIR, download_video_task


async def get_api_version():
    return {
        'version': '0.2.0',
    }

async def download_video(url: str = Query(...)) -> dict:
    job_id = str(uuid.uuid4())
    download_video_task.delay(url, job_id)

    return {"job_id": job_id, "status": "processing"}

async def check_status(job_id: str) -> dict:
    filepath = os.path.join(DOWNLOAD_DIR, f"{job_id}.mp4")
    log_path = os.path.join(DOWNLOAD_DIR, f"{job_id}.log")
    if os.path.exists(log_path):
        return {"status": "failed"}
    if os.path.exists(filepath):
        return {
            "status": "completed",
            "download_url": filepath,
        }

    return {"status": "processing"}

async def get_file(filename: str) -> FileResponse:
    filepath = os.path.join(DOWNLOAD_DIR, f"{filename}.mp4")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not ready yet")

    return FileResponse(filepath, filename=f"{filename}.mp4", media_type="video/mp4")
