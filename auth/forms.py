from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField("Email", [DataRequired(), Email("This field requires a valid email address")])
    password = PasswordField("Password", [DataRequired()])
    remeber_me = BooleanField("Remember Me")
