from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class GroupCreateForm(FlaskForm):
    name = StringField("Group Name", [DataRequired(), Length(min=5, max=100, message="Name must be at least 5 characters long")])


class GroupDeleteForm(FlaskForm):
    pass
