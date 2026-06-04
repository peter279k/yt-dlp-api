from .video import *
from fastapi import APIRouter


info_router = APIRouter(tags=['API version'])
info_router.add_api_route('/', get_api_version, methods=['GET'])

video_info_router = APIRouter(tags=['Download video with Message Queue Approach'])
video_info_router.add_api_route('/download/', download_video, methods=['GET'])
video_info_router.add_api_route('/status/{job_id}', check_status, methods=['GET'])
video_info_router.add_api_route('/files/{filename}', get_file, methods=['GET'])
