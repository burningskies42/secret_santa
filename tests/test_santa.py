import os
import tempfile
import pytest

from secret_santa import create_app, db
from secret_santa.models import Address, Group, Member, User


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
    app = create_app(TEST_SQLILE_PATH=f"sqlite:///{path_temp_db}_santa.sqlite")
    app.config["TESTING"] = True
    app.config["CSRF_ENABLED"] = False
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.create_all()
        db.session.commit()

    yield app

    os.close(db_fd)
    os.unlink(path_temp_db)


@pytest.fixture
def client(app):
    """Define fixture for client so that it can be called by comming test."""

    return app.test_client()


def test_1_1_index_html_status_code(client, app):
    """
    Test the main page reachability and assert it's status code to be '200'.
    Following methods should be valid:
        * GET
    """

    assert client.get('/').status_code == 200


def test_1_2_index_html_context(client, app):
    """Test the main page reachability and assert it's context to be some kind of html."""

    resp = client.get('/')
    assert b"<!DOCTYPE html>" in resp.data
    assert resp.mimetype == MIME_TYPES["html"]


def test_2_1_signup(client, app):
    """Test the registration process:
        * GET '/users/create' endpoint
        * POST '/users/create' endpoint with valid registration data
        * check if user was added to db.Users
    """

    user_data = {
        "name": "Some User Name",
        "email": "some_email@domain.com",
        "password": "12345qwertzui$",
        "address": "Some Adress 123"
    }

    assert client.get("/users/create").status_code == 200
    assert client.post("/users/create", data=user_data, follow_redirects=True).status_code == 200
    with app.app_context():
        assert User.query.filter_by(email=user_data["email"]).first().name == user_data["name"]
