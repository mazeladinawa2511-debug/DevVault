
from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Project
from app.projects.forms import ProjectForm


projects = Blueprint("projects", __name__, url_prefix="/projects")


@projects.route("/")
@login_required
def index():
    user_projects = db.session.scalars(
        db.select(Project)
        .where(Project.user_id == current_user.id)
        .order_by(Project.created_at.desc())
    ).all()

    return render_template(
        "projects/index.html",
        projects=user_projects,
    )


@projects.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = ProjectForm()

    if form.validate_on_submit():
        project = Project(
            name=form.name.data.strip(),
            description=(form.description.data or "").strip(),
            user_id=current_user.id,
        )

        db.session.add(project)
        db.session.commit()

        flash("Project created successfully.", "success")
        return redirect(url_for("projects.index"))

    return render_template("projects/create.html", form=form)



@projects.route("/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit(project_id):
    project = db.session.scalar(
        db.select(Project).where(
            Project.id == project_id,
            Project.user_id == current_user.id,
        )
    )

    if project is None:
        abort(404)

    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        project.name = form.name.data.strip()
        project.description = (form.description.data or "").strip()

        db.session.commit()

        flash("Project updated successfully.", "success")
        return redirect(url_for("projects.index"))

    return render_template(
        "projects/edit.html",
        form=form,
        project=project,
    )


@projects.route("/<int:project_id>/delete", methods=["POST"])
@login_required
def delete(project_id):
    project = db.session.scalar(
        db.select(Project).where(
            Project.id == project_id,
            Project.user_id == current_user.id,
        )
    )

    if project is None:
        abort(404)

    db.session.delete(project)
    db.session.commit()

    flash("Project deleted successfully.", "success")
    return redirect(url_for("projects.index"))
