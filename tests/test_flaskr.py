from flask import (Flask, url_for, redirect)
import pytest
from app import app
# app = Flask(__name__)
# import app


@pytest.fixture
def client():
    return app.test_client()


def test_response_html(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'


def posting(client, short_url, long_url):
    return client.post('/', data=dict(
        short_url = 'short_url',
        long_url = 'long_url'
    ))

def test_post(client):
    rv = posting(client, app.config['short_url'], app.config['long_url'])
    assert b"this was posted" in rv.data
























# import tempfile
# import pytest
# from flaskr import flaskr

# @pytest.fixture
# def client():
#     #tempfile.mkstemp() 
#     db_fd, flaskr.app.config['DATABASE'] = 'sqlite:///test.db'
#     flaskr.app.config['TESTING'] = True

#     with flaskr.app.test_client() as client:
#         with flaskr.app.app_context():
#             flaskr.init_db()
#         yield client

#     os.close(db_fd)
#     os.unlink(flaskr.app.config['DATABASE'])

# def test_empty_db(client):
#     """Start with a blank database."""
#     rv = client.get('/')
#     assert b'There are no tasks create one below:' in rv.data