from flask import Blueprint, make_response, redirect, render_template, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

# from .utils.db import Connection
from .models import Users
from . import db


auth = Blueprint("auth", __name__)

# Routes for handling the signup/login/logout pages
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


@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    remember = True if request.form.get('remember') else False
    user = Users.query.filter_by(email=request.form.get('email')).first()
    if not user or not check_password_hash(user.password, request.form.get('password')):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('users.profile', user_id=user.id))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
