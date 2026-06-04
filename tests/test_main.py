from app.main import app
from unittest.mock import patch
from fastapi.testclient import TestClient


client = TestClient(app)

def test_get_api_version():
    response = client.get('/')

    assert response.status_code == 200
    assert response.json()['version'] == '0.2.0'
    assert response.json() == {'version': '0.2.0'}

def test_docs_available():
    response = client.get('/docs')

    assert response.status_code == 200

def test_download_endpoint_returns_job_id():
    with patch('app.workers.worker.download_video_task.delay') as mock_task:
        response = client.get('/download/', params={'url': 'https://example.com/video'})

    assert response.status_code == 200

    data = response.json()
    assert 'job_id' in data
    assert data['status'] == 'processing'
    mock_task.assert_called_once()

def test_status_processing() -> None:
    response = client.get('/status/fake-job-id')
    assert response.status_code == 200

    data = response.json()
    assert 'status' in data

def test_file_not_found() -> None:
    response = client.get('/files/nonexistent.mp4')

    assert response.status_code in (200, 404)
