
import pytest

from app import create_app
from app.extensions import db
from app.models import Project, User


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


def create_user(username="mazel", email="mazel@example.com"):
    user = User(username=username, email=email)
    user.set_password("StrongPassword123!")

    db.session.add(user)
    db.session.commit()

    return user


def test_project_model_can_be_saved(client):
    with client.application.app_context():
        user = create_user()

        project = Project(
            name="DevVault",
            description="Developer project management",
            user_id=user.id,
        )

        db.session.add(project)
        db.session.commit()

        saved = db.session.get(Project, project.id)

        assert saved is not None
        assert saved.name == "DevVault"
        assert saved.status == "active"
        assert saved.user_id == user.id


def test_projects_require_login(client):
    response = client.get("/projects/")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_create_project_requires_login(client):
    response = client.get("/projects/new")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_logged_in_user_can_create_project(client):
    with client.application.app_context():
        create_user()

    login_response = client.post(
        "/login",
        data={
            "username": "mazel",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 302

    response = client.post(
        "/projects/new",
        data={
            "name": "My First Project",
            "description": "A test project",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"My First Project" in response.data

    with client.application.app_context():
        project = db.session.scalar(
            db.select(Project).where(
                Project.name == "My First Project"
            )
        )

        assert project is not None
        assert project.user_id is not None



def test_user_cannot_edit_another_users_project(client):
    with client.application.app_context():
        create_user("owner", "owner@example.com")
        other_user = create_user("other", "other@example.com")

        project = Project(
            name="Private Project",
            description="Belongs to another user",
            user_id=other_user.id,
        )
        db.session.add(project)
        db.session.commit()
        project_id = project.id

    client.post(
        "/login",
        data={
            "username": "owner",
            "password": "StrongPassword123!",
        },
    )

    response = client.get(f"/projects/{project_id}/edit")

    assert response.status_code == 404


def test_user_cannot_delete_another_users_project(client):
    with client.application.app_context():
        create_user("owner", "owner@example.com")
        other_user = create_user("other", "other@example.com")

        project = Project(
            name="Private Project",
            description="Belongs to another user",
            user_id=other_user.id,
        )
        db.session.add(project)
        db.session.commit()
        project_id = project.id

    client.post(
        "/login",
        data={
            "username": "owner",
            "password": "StrongPassword123!",
        },
    )

    response = client.post(f"/projects/{project_id}/delete")

    assert response.status_code == 404

    with client.application.app_context():
        saved_project = db.session.get(Project, project_id)
        assert saved_project is not None
