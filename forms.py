from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

class UserForm(FlaskForm):
    name = StringField("Full Name", [DataRequired()])
    address = StringField("Address", [DataRequired()])
    email = StringField("Email", [DataRequired(), Email("This field requires a valid email address")])
    password = PasswordField("Password", [DataRequired()])
