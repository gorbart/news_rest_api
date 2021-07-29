import json

from starlette.testclient import TestClient

from app.server.app import app

ARTICLE_ID = '6102a884c0e5cf8805822e7a'
SAMPLE_ARTICLE_DICT = {
    'title': 'title',
    'text': 'text',
    'publication_time': '2021-07-29T11:30',
    'source': 'source',
    'author': '6102ab9eec2d3690aa7677b0'
}

client = TestClient(app)


def test_get_articles():
    response = client.get('/article/')

    assert response.status_code == 200


def test_get_articles_for_author():
    response = client.get(f"/article/author/{SAMPLE_ARTICLE_DICT['author']}")

    assert response.status_code == 200


def test_get_article():
    response = client.get(f'/article/{ARTICLE_ID}')

    assert response.status_code == 200
    assert response.json()['text'] == 'text'


def test_get_nonexistent_article():
    response = client.get(f"/article/{ARTICLE_ID.replace('6', '7')}")

    assert response.status_code == 404


def test_add_article():
    response = client.post('/article/', json=SAMPLE_ARTICLE_DICT)

    assert response.status_code == 201
    assert json.loads(response.json())['text'] == 'text'


def test_update_article():
    add_response = client.post('/article/', json=SAMPLE_ARTICLE_DICT)

    article_id = json.loads(add_response.json())['_id']['$oid']

    put_response = client.put(f'/article/{article_id}', json={'text': 'ttttteeeeexxxxxtttttt'})

    assert put_response.status_code == 200

    get_response = client.get(f'/article/{article_id}')

    assert get_response.json()['text'] == "ttttteeeeexxxxxtttttt"


def test_update_article_without_arguments():
    put_response = client.put(f'/article/{ARTICLE_ID}', json={})

    assert put_response.status_code == 202


def test_delete_article():
    add_response = client.post('/article/', json=SAMPLE_ARTICLE_DICT)

    article_id = json.loads(add_response.json())['_id']['$oid']

    delete_response = client.delete(f'/article/{article_id}')

    assert delete_response.status_code == 204
