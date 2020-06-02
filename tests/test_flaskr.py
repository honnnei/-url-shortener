import tempfile
import pytest
from flaskr import flaskr

@pytest.fixture
def client():
    #tempfile.mkstemp() 
    db_fd, flaskr.app.config['DATABASE'] = 'sqlite:///test.db'
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            flaskr.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'There are no tasks create one below:' in rv.data