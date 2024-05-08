#test_app.py
import pytest
import json
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the CRUD API!' in response.data


def test_create_item(client):
    data = {'name': 'Test Item', 'description': 'This is a test item'}
    response = client.post('/items', json=data)
    assert response.status_code == 200
    assert 'error' not in json.loads(response.data)

def test_get_all_items(client):
    response = client.get('/items')
    assert response.status_code == 200
    assert 'error' not in json.loads(response.data)

def test_get_item(client):
    data = {'name': 'Test Item', 'description': 'This is a test item'}
    response_create = client.post('/items', json=data)
    item_id = json.loads(response_create.data)

    response_get = client.get(f'/items/{item_id}')
    assert response_get.status_code == 200
    assert 'error' not in json.loads(response_get.data)

def test_update_item(client):
    data = {'name': 'Test Item', 'description': 'This is a test item'}
    response_create = client.post('/items', json=data)
    item_id = json.loads(response_create.data)

    updated_data = {'description': 'Updated description'}
    response_update = client.put(f'/items/{item_id}', json=updated_data)
    assert response_update.status_code == 200
    assert 'error' not in json.loads(response_update.data)

def test_delete_item(client):
    data = {'name': 'Test Item', 'description': 'This is a test item'}
    response_create = client.post('/items', json=data)
    item_id = json.loads(response_create.data)

    response_delete = client.delete(f'/items/{item_id}')
    assert response_delete.status_code == 200
    assert 'error' not in json.loads(response_delete.data)

