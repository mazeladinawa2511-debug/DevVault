from datetime import datetime, timezone

from app.extensions import db


def utc_now():
    return datetime.now(timezone.utc)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    owner = db.relationship(
        "User",
        backref=db.backref(
            "projects",
            lazy=True,
            cascade="all, delete-orphan",
        ),
    )

    name = db.Column(
        db.String(120),
        nullable=False,
        index=True
    )

    description = db.Column(
        db.Text,
        nullable=False,
        default=""
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="active"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    def __repr__(self):
        return f"<Project {self.id}: {self.name}>"
