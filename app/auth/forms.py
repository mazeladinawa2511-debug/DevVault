from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=40),
        ],
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=255),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=12, max=128),
        ],
    )

    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password"),
        ],
    )

    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )

    remember = BooleanField("Remember me")

    submit = SubmitField("Sign in")
