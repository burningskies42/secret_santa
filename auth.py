from flask import Blueprint, make_response, redirect, render_template, request, url_for, flash
from flask_login import login_user

# from .utils.db import Connection
from utils import add_user, login_user


auth = Blueprint('auth', __name__)

# Route for handling the login page logic
@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    response, _cookies = login_user(
        request.form["user_login"],
        request.form["user_password"],
        request.remote_addr
    )

    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    return render_template("signup.html")


@auth.route('/signup', methods=['POST'])
def signup_post():
    if add_user(request.form) is not None:
        flash('Email address already exists')

        return render_template("signup.html")

    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    return 'Logout'