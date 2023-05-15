from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_get_api_version():
    response = client.get('/')

    assert response.status_code == 200
    assert response.json()['version'] == '0.1.0'
    assert response.json() == {'version': '0.1.0'}

def test_extract_video_info_on_invalid_url():
    invalid_url = 'https://invalid.url'
    response = client.get('/video?video_url=%s' % invalid_url)

    assert response.status_code == 200
    assert response.json()['error'] == 'Unsupported %s!' % invalid_url
