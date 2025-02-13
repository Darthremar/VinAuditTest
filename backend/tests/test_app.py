import pytest
from ..app.app import create_app
from ..app.config import Config

@pytest.fixture
def app():
    app = create_app(Config)
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Search Vehicles" in response.data

def test_search_functionality(client):
    response = client.post('/', data={'year': '2020', 'make': 'Toyota', 'model': 'Camry'})
    assert response.status_code == 200
    assert b"Estimated market price" in response.data

def test_search_page(client):
    response = client.get('/search')
    assert response.status_code == 200

def test_results_page(client):
    response = client.get('/results')
    assert response.status_code == 200

def test_search_form_empty(client):
    response = client.post('/search', data={'year': '', 'make': '', 'model': ''})
    assert response.status_code == 400

def test_search_form(client):
    response = client.post('/search', data={'year': '2020', 'make': 'Toyota', 'model': 'Camry'})
    assert response.status_code == 200

def test_search_from_mileage(client):
    response = client.post('/search', data={'year': '2020', 'make': 'Toyota', 'model': 'Camry', 'mileage': 10000})
    assert response.status_code == 200

def test_search_form_invalid_year(client):
    response = client.post('/search', data={'year': 2020, 'make': 'Toyota', 'model': 'Camry'})
    assert response.status_code == 400

def test_search_form_invalid_make(client):
    response = client.post('/search', data={'year': '2020', 'make': True, 'model': 'Camry'})
    assert response.status_code == 400

def test_search_form_invalid_model(client):
    response = client.post('/search', data={'year': '2020', 'make': 'Toyota', 'model': True})
    assert response.status_code == 400

if __name__ == '__main__':
    pytest.main() 