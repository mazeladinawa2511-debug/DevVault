from flask import Flask

from config import Config
from app.extensions import db, migrate, login_manager, csrf
from flask_login import current_user
from app.models import User
from app.auth.routes import auth
from app.projects.routes import projects

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    app.register_blueprint(auth)
    app.register_blueprint(projects)

    # Route halaman utama tetap di sini
    @app.route("/")
    def index():
        return {
            "app": "DevVault",
            "status": "running",
            "version": "0.1.0"
        }

    return app
