from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from secret_santa.auth.forms import LoginForm
from ..models import User


auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates"
)


# Routes for handling the signup/login/logout pages
@auth.route("/login")
def login():
    login_form = LoginForm()
    return render_template("auth/login.html", title="Login", form=login_form)


@auth.route('/login', methods=['POST'])
def login_post():
    # from IPython import embed; embed()
    remember = True if request.form.get('remember_me') else False
    user = User.query.filter_by(email=request.form.get('email')).first()
    if not user or not check_password_hash(user.password, request.form.get('password')):
        flash("Please check your login details and try again.", "is-danger")
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('users.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout successful!", "is-success")
    return redirect(url_for('main.index'))
