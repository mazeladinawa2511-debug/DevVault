from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import login_user, logout_user
from sqlalchemy import or_

from app.extensions import db
from app.models import User
from app.auth.forms import RegistrationForm, LoginForm


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()

        existing_user = db.session.scalar(
            db.select(User).where(
                or_(
                    User.username == username,
                    User.email == email,
                )
            )
        )

        if existing_user:
            flash("Username or email is already registered.", "error")
            return render_template("auth/register.html", form=form), 409

        user = User(
            username=username,
            email=email,
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Account created. You can now sign in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data.strip()

        user = db.session.scalar(
            db.select(User).where(
                User.username == username
            )
        )

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.", "error")
            return render_template("auth/login.html", form=form), 401

        login_user(user, remember=form.remember.data)
        flash("Signed in successfully.", "success")
        return redirect(url_for("index"))

    return render_template("auth/login.html", form=form)


@auth.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("You have signed out.", "success")
    return redirect(url_for("auth.login"))
