import pytest

from app import create_app
from app.extensions import db
from app.models import User


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


@pytest.fixture
def client():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


def test_register_page_loads(client):
    response = client.get("/register")

    assert response.status_code == 200


def test_login_page_loads(client):
    response = client.get("/login")

    assert response.status_code == 200


def test_logout_requires_post(client):
    response = client.get("/logout")

    assert response.status_code == 405


def test_register_creates_user(client):
    response = client.post(
        "/register",
        data={
            "username": "mazel",
            "email": "mazel@example.com",
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    user = db.session.scalar(
        db.select(User).where(User.username == "mazel")
    )

    assert user is not None
    assert user.email == "mazel@example.com"
    assert user.password_hash != "StrongPassword123!"


def test_login_with_wrong_password_fails(client):
    with client.application.app_context():
        user = User(
            username="mazel",
            email="mazel@example.com",
        )
        user.set_password("StrongPassword123!")

        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/login",
        data={
            "username": "mazel",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert b"Invalid username or password." in response.data

def test_login_with_correct_password_succeeds(client):
    with client.application.app_context():
        user = User(
            username="mazel",
            email="mazel@example.com",
        )
        user.set_password("StrongPassword123!")

        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/login",
        data={
            "username": "mazel",
            "password": "StrongPassword123!",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
