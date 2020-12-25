from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class UserCreateForm(FlaskForm):
    name = StringField("Full Name", [DataRequired(), Length(min=5, max=100, message="Name must be at least 5 characters long")])
    address = StringField("Address", [DataRequired(), Length(min=5, max=100, message="Address must be at least 5 characters long")])
    email = StringField("Email", [DataRequired(), Email("This field requires a valid email address")])
    password = PasswordField("Password", [DataRequired()])


class UserEditForm(FlaskForm):
    name = StringField("Full Name", [DataRequired(), Length(min=5, max=100, message="Name must be at least 5 characters long")])
    address = StringField("Address", [DataRequired(), Length(min=5, max=100, message="Address must be at least 5 characters long")])
    email = StringField("Email", [DataRequired(), Email("This field requires a valid email address")])


class UserDeleteForm(FlaskForm):
    # since we do not have any fields in our form, we will just pass here
    # we are only creating this class so we can inherit from FlaskForm and get built-in CSRF protection
    pass
