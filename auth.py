from flask import Blueprint, make_response, redirect, render_template, request, url_for, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

# from .utils.db import Connection
from utils import add_user, log_in_user
from .models import Users
from . import db


auth = Blueprint('auth', __name__)

# Route for handling the login page logic
@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    # remember = True if request.form.get('remember') else False
    user = Users.query.filter_by(email=request.form.get('email')).first()
    print(f"User: {user}")
    if not user or not check_password_hash(user.password, request.form.get('password')):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    return render_template("signup.html")


@auth.route('/signup', methods=['POST'])
def signup_post():
    user = Users.query.filter_by(email=request.form.get("email")).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = Users(
        email=request.form.get("email"),
        name=request.form.get("name"),
        password=generate_password_hash(request.form.get("password"), method='sha256')
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    return 'Logout'