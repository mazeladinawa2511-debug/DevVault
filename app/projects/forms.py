from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ProjectForm(FlaskForm):
    name = StringField(
        "Project name",
        validators=[
            DataRequired(),
            Length(min=3, max=120),
        ],
    )

    description = TextAreaField(
        "Description",
        validators=[
            Length(max=5000),
        ],
    )

    submit = SubmitField("Save project")
