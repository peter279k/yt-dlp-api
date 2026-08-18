import os
import tempfile
from pathlib import Path

import yt_dlp
from celery import Celery
from playwright.sync_api import sync_playwright

DOWNLOAD_DIR = Path('/app/downloads/')
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

celery = Celery(
    "worker",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="rpc://",
)

def get_cookie_from_playwright():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        page.goto("https://www.youtube.com")
        page.wait_for_load_state("networkidle")
        
        playwright_cookies = context.cookies()
        browser.close()

        netscape_lines = ["# Netscape HTTP Cookie File\n# http://haxx.se\n# This is a generated file! Do not edit.\n\n"]
        
        for cookie in playwright_cookies:
            if "youtube.com" in cookie["domain"]:
                domain = cookie["domain"]
                include_subdomains = "TRUE" if domain.startswith(".") else "FALSE"
                path = cookie["path"]
                secure = "TRUE" if cookie["secure"] else "FALSE"
                expires = str(int(cookie.get("expires", 0))) if cookie.get("expires") is not None else "0"
                name = cookie["name"]
                value = cookie["value"]

                line = f"{domain}\t{include_subdomains}\t{path}\t{secure}\t{expires}\t{name}\t{value}\n"
                netscape_lines.append(line)
                
        return "".join(netscape_lines)

@celery.task
def download_video_task(url: str, job_id: str) -> str:
    cookie_content = get_cookie_from_playwright()

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_cookie_file:
        temp_cookie_file.write(cookie_content)
        temp_cookie_path = temp_cookie_file.name

    filepath = os.path.join(DOWNLOAD_DIR, f"{job_id}.mp4")
    ydl_opts = {
        'cookiefile': temp_cookie_path,
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
