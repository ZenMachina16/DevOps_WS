import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_welcome(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Library API' in response.data

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'OK'

def test_get_all_books(client):
    response = client.get('/api/books')
    assert response.status_code == 200
    data = response.get_json()
    assert 'books' in data
    assert isinstance(data['books'], list)

def test_get_book_by_id_success(client):
    response = client.get('/api/books/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'title' in data

def test_get_book_by_id_not_found(client):
    response = client.get('/api/books/9999')
    assert response.status_code == 404
    assert b'not found' in response.data.lower()

def test_post_new_book(client):
    new_book = {
        "title": "Zero to One",
        "author": "Peter Thiel",
        "genre": "Business",
        "year": 2014
    }
    response = client.post('/api/books', json=new_book)
    assert response.status_code == 201
    data = response.get_json()
    assert data['book']['title'] == new_book['title']

def test_update_book(client):
    update_data = {
        "title": "Updated Title"
    }
    response = client.put('/api/books/1', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['book']['title'] == "Updated Title"

def test_delete_book(client):
    response = client.delete('/api/books/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'deleted' in data['message'].lower()

def test_api_info(client):
    response = client.get('/api/info')
    assert response.status_code == 200
    data = response.get_json()
    assert data['project_name'] == 'Library API'