import os


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-only-change-this-before-deployment"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///devvault.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
