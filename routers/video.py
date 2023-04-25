import yt_dlp
from urllib.parse import urlparse


async def get_api_version():
    return {
        'version': '0.1.0',
    }

async def extract_video_info(video_url: str = ''):
    ydl_opts = {
        'quiet': True,
        'simulate': True,
    }

    response = {'error': None}

    parsed_url_result = urlparse(video_url)
    if parsed_url_result.netloc != 'www.youtube.com':
        response['error'] = 'Unsupported %s!' % parsed_url_result.netloc

        return response

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url)

            response = {'links': []}
            for format_lists in info['formats']:
                if format_lists['acodec'] != 'none' and format_lists['vcodec'] != 'none' and format_lists['resolution'] != 'audio only' and format_lists['ext'] == 'mp4':
                    response['links'].append({
                        'format': format_lists['ext'],
                        'itag': format_lists['resolution'] + '(' + str(format_lists['aspect_ratio']) + ')',
                        'url': format_lists['url'],
                    })

        except Exception as e:
            response['error'] = str(e)


    return response
