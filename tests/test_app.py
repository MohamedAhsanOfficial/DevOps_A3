import pytest

from app import create_app
from app.models import db, Note


@pytest.fixture
def app_instance():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app_instance):
    return app_instance.test_client()


def test_home_page_shows_empty_state(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Capture a quick note" in response.data
    assert b"No notes yet" in response.data


def test_form_submission_stores_note(client, app_instance):
    payload = {"title": "CI Tip", "body": "Automate cleanup"}
    response = client.post("/", data=payload, follow_redirects=True)
    assert response.status_code == 200
    assert b"Note saved" in response.data

    with app_instance.app_context():
        note = Note.query.filter_by(title="CI Tip").first()
        assert note is not None
        assert note.body == "Automate cleanup"
