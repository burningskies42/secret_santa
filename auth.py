from flask import Blueprint, make_response, redirect, render_template, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

# from .utils.db import Connection
from .models import Users
from . import db

from loguru import logger


auth = Blueprint("auth", __name__)

# Routes for handling the signup/login/logout pages

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
