import os
import tempfile
import pytest
from secret_santa import create_app


MIME_TYPES = {
    "html": "text/html"
}

@pytest.fixture
def app():
    """
    Define fixture for app to be used by client. For the purpose of the tests some random
    database is generated and deleted after the last test.
    """

    db_fd, path_temp_db = tempfile.mkstemp()
    app = create_app(TEST_SQLILE_PATH=path_temp_db)
    yield app

    os.close(db_fd)
    os.unlink(path_temp_db)


@pytest.fixture
def client(app):
    """Define fixture for client so that it can be called by comming test."""

    return app.test_client()


def test_index_html_status_code(client, app):
    """
    Test the main page reachability and assert it's status code to be '200'.
    Following methods should be valid:
        * GET
    """

    resp_get = client.get('/')
    assert resp_get.status_code == 200


def test_index_html_context(client, app):
    """Test the main page reachability and assert it's context to be some kind of html."""

    resp = client.get('/')
    assert b"<!DOCTYPE html>" in resp.data
    assert resp.mimetype == MIME_TYPES["html"]
