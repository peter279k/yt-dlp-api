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

def test_extract_video_info_on_mocked_valid_url(mocker):
    expected = {
        'links': [
            {
                'format': 'mp4',
                'itag': '640x360(1.78)',
                'url': 'https://rr2---sn-npoe7nsy.googlevideo.com/videoplayback?expire=1684161452&ei=TO9hZNWuEMiZ4t4Pzpm7wAI&ip=128.199.97.204&id=o-AIPOHKMTPqbKPfTF_Cq9ZSoMzBU2iVeQvxHY2WO1Ym1X&itag=18&source=youtube&requiressl=yes&mh=vn&mm=31%2C26&mn=sn-npoe7nsy%2Csn-un57enel&ms=au%2Conr&mv=m&mvi=2&pl=18&initcwndbps=192500&spc=qEK7B_EbwPGy3BrcjHT_ZI71fEugKoE&vprv=1&svpuc=1&mime=video%2Fmp4&gir=yes&clen=6396943&ratebypass=yes&dur=271.952&lmt=1683722090394684&mt=1684139583&fvip=4&fexp=24007246%2C51000022&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRAIgM9Kp-e5J4Cq9m2GA_RmfcSSse0YJTg8NmnXWi1TMVXcCIHx_RdyYXsftuUwQo2a-3GY4yXSlvfBZVoCzTem4CsXD&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhAKL3jZXOgkn46xqqRjlawFt2MZm58SpRp5VjGiLin-ExAiBQFrJ7VJqwrF353pAk0cgZJkALb8-0EJf2y1QIh7pWjA%3D%3D'
            },
            {
                'format': 'mp4',
                'itag': '1280x720(1.78)',
                'url': 'https://rr2---sn-npoe7nsy.googlevideo.com/videoplayback?expire=1684161452&ei=TO9hZNWuEMiZ4t4Pzpm7wAI&ip=128.199.97.204&id=o-AIPOHKMTPqbKPfTF_Cq9ZSoMzBU2iVeQvxHY2WO1Ym1X&itag=22&source=youtube&requiressl=yes&mh=vn&mm=31%2C26&mn=sn-npoe7nsy%2Csn-un57enel&ms=au%2Conr&mv=m&mvi=2&pl=18&initcwndbps=192500&spc=qEK7B_EbwPGy3BrcjHT_ZI71fEugKoE&vprv=1&svpuc=1&mime=video%2Fmp4&cnr=14&ratebypass=yes&dur=271.952&lmt=1683722208235885&mt=1684139583&fvip=4&fexp=24007246%2C51000022&c=ANDROID&txp=5318224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIhANYe1IhkGKzmL7mwmxbYIE9OK_HDKaKhE-GRnltn-RAWAiBuAjr8wmkvIu8FrCEvbndNRjnouVPTbJvTaBS7ZYPh_Q%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhAKL3jZXOgkn46xqqRjlawFt2MZm58SpRp5VjGiLin-ExAiBQFrJ7VJqwrF353pAk0cgZJkALb8-0EJf2y1QIh7pWjA%3D%3D'
            },
        ]
    }

    valid_url = 'https://www.youtube.com/watch?v=oYS28kmur2k'
    mocker.patch(
        'fastapi.testclient.TestClient.get',
        return_value=expected
    )

    actual = client.get(valid_url)
    assert expected == actual
