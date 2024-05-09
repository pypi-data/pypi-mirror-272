import pytest
import requests_mock
from src.docta_http_client import DoctaHTTPClient

@pytest.fixture
def client():
    return DoctaHTTPClient(api_key='test_api_key', user_id='test_user_id')

def test_model_set_get(client):
    assert client.get_model() is None  # Initially, should be None
    client.set_model('user')
    assert client.get_model() == 'user'  # After setting, should return 'user'

def test_run_docta_with_model(client):
    client.set_model('user')
    with requests_mock.Mocker() as m:
        m.post('https://staging.api.docta.ai/api-key-language-safety', json={'result': 'success'}, status_code=200)
        response = client.run_docta(data={'name': 'Alice'})
        assert response == {'result': 'success'}

def test_run_docta_without_model(client):
    with pytest.raises(ValueError) as excinfo:
        client.run_docta(data={'name': 'Alice'})
    assert "model is not set" in str(excinfo.value)  # Expected error if model is not set
