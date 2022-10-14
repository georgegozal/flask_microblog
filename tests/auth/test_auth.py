from flask_login import current_user
from werkzeug.security import check_password_hash

APP_URLS = [
    '/',
    '/api/posts',
    '/api/users',
    '/login',
    '/user/add',
]


def test_urls(client):
    for url in APP_URLS:
        response = client.get(url)
        assert response.status_code == 200


def test_redirect(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert response.request.path == '/login'


def test_login(client):
    assert client.get('/login').status_code == 200

    with client:
        client.post('/login',data={'username': 'test_user','password': 'password123'})
        assert current_user.is_authenticated


def test_failed_register(client):
    assert client.get('/user/add').status_code == 200
    response = client.post('/user/add', 
        data={'username': "pytest", 'name': 'test', "email": "test_userEmail0555@mail.com",
                "password_hash": "password5", "password_hash2": "password7"}, 
                    follow_redirects=True)
    assert b"Passwords Must Match!" in response.data


def test_successful_register(client):
    assert client.get('/user/add').status_code == 200
    response = client.post('/user/add', 
        data={'username': "pytest", 'name': 'test', "email": "test_userEmail0555@mail.com",
                "password_hash": "password5", "password_hash2": "password5"}, 
                    follow_redirects=True)
    assert response.request.path == '/dashboard'
