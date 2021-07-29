import json

from starlette.testclient import TestClient

from app.server.app import app

AUTHOR_ID = '6102ab9eec2d3690aa7677b0'
SAMPLE_AUTHOR_DICT = {
    'name': 'name',
    'surname': 'surname',
    'website': 'website'
}

client = TestClient(app)


def test_get_authors():
    response = client.get('/author/')

    assert response.status_code == 200


def test_get_author():
    response = client.get(f'/author/{AUTHOR_ID}')

    assert response.status_code == 200
    assert response.json()['name'] == 'name'


def test_get_nonexistent_author():
    response = client.get(f"/author/{AUTHOR_ID.replace('6', '7')}")

    assert response.status_code == 404


def test_add_author():
    response = client.post('/author/', json=SAMPLE_AUTHOR_DICT)

    assert response.status_code == 201
    assert json.loads(response.json())['name'] == 'name'


def test_update_author():
    add_response = client.post('/author/', json=SAMPLE_AUTHOR_DICT)

    author_id = json.loads(add_response.json())['_id']['$oid']

    put_response = client.put(f'/author/{author_id}', json={'name': 'nnnnaaaammmmeeeee'})

    assert put_response.status_code == 200

    get_response = client.get(f'/author/{author_id}')

    assert get_response.json()['name'] == "nnnnaaaammmmeeeee"


def test_update_author_without_arguments():
    put_response = client.put(f'/author/{AUTHOR_ID}', json={})

    assert put_response.status_code == 202


def test_delete_author():
    add_response = client.post('/author/', json=SAMPLE_AUTHOR_DICT)

    author_id = json.loads(add_response.json())['_id']['$oid']

    delete_response = client.delete(f'/author/{author_id}')

    assert delete_response.status_code == 204
