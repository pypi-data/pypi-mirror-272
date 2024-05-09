import pytest
import requests_mock
from src.base_client import APIClient

@pytest.fixture
def api_client():
    return APIClient(api_key='fake_api_key', user_id='fake_user_id')

def test_get_successful(api_client):
    with requests_mock.Mocker() as m:
        m.get('https://staging.api.docta.ai/api-key-language-safety', json={'success': True}, status_code=200)
        response = api_client.get('model_name', params={'key': 'value'})
        assert response == {'success': True}

def test_post_successful(api_client):
    with requests_mock.Mocker() as m:
        m.post('https://staging.api.docta.ai/api-key-language-safety', json={'posted': True}, status_code=200)
        response = api_client.post('model_name', data={'key': 'value'})
        assert response == {'posted': True}
