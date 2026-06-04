from app.routers import *
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware


description = '''
yt_dlp API Server

## Features

You can look at the following lists:

## Extract video info

- Extracting the YouTube video info with the specific video URL
'''

api_version = '0.2.0'
app = FastAPI(
    title='yt_dlp API Server',
    description=description,
    version=api_version,
    contact={
        'name': 'Peter',
        'email': 'peter279k@gmail.com',
    },
)

origins = ['*']

app.mount('/web', StaticFiles(directory='/app/app/web'), name='web')
app.include_router(info_router)
app.include_router(video_info_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=origins,
    allow_headers=origins,
)

@app.middleware('http')
async def check_x_token_header(request: Request, call_next):
    if request.method == 'OPTIONS':
        return await call_next(request)

    return await call_next(request)

add_pagination(app)
