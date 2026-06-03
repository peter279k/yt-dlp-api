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

async def extract_video_info(video_url: str = ''):
    ydl_opts = {
        'quiet': True,
        'simulate': True,
    }

    response = {'error': None}

    parsed_url_result = urlparse(video_url)
    if parsed_url_result.netloc != 'www.youtube.com':
        response['error'] = 'Unsupported %s!' % video_url

        return response

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url)

            response = {'links': []}
            for format_lists in info['formats']:
                if format_lists.get('acodec') is None:
                    continue
                if format_lists['audio_ext'] == 'm4a' and 'videoplayback?' in format_lists['url']:
                    response['links'].append({
                        'format': format_lists['ext'],
                        'itag': format_lists['resolution'] + '(' + str(format_lists['aspect_ratio']) + ')',
                        'url': format_lists['url'],
                    })
                elif format_lists['video_ext'] == 'mp4' and 'videoplayback?' in format_lists['url']:
                    response['links'].append({
                        'format': format_lists['ext'],
                        'itag': format_lists['resolution'] + '(' + str(format_lists['aspect_ratio']) + ')',
                        'url': format_lists['url'],
                    })

        except Exception as e:
            response['error'] = str(e)


    return response

async def download_video(url: str = Query(...)) -> dict:
    job_id = str(uuid.uuid4())
    download_video_task.delay(url, job_id)

    return {"job_id": job_id, "status": "processing"}

async def check_status(job_id: str) -> dict:
    filepath = os.path.join(DOWNLOAD_DIR, f"{job_id}.mp4")
    if os.path.exists(filepath):
        return {
            "status": "completed",
            "download_url": filepath,
        }

    return {"status": "processing"}

async def get_file(filename: str) -> FileResponse:
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not ready yet")

    return FileResponse(filepath, filename=filename, media_type="video/mp4")
