from flask_login import current_user


def test_posts(client):
    response = client.get('/add-post', follow_redirects=True)
    assert response.request.path == '/login'

    with client:
        client.post('/login',data={'username': 'admin','password': 'admin'})
        assert current_user.is_authenticated

        assert client.get('/add-post').status_code == 200
        response = client.post('/add-post',
            data={'title': 'Pytest Blog Post.',
                'content': 'The pytest framework makes it easy to write small, \
                    readable tests, and can scale to support complex functional testing for \
                        applications and libraries.',
                'poster_id': current_user.id
            })
