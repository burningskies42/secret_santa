from loguru import logger
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from .forms import UserForm
from . import db


users = Blueprint("users", __name__)


@users.route('/new')
def signup():
    user_form = UserForm()
    return render_template("signup.html", form=user_form)

@users.route('/new', methods=['POST'])
def signup_post():
    logger.debug(request.form)
    user = Users.query.filter_by(email=request.form.get("email")).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('users.signup'))

    user_form = UserForm(request.form)
    # from IPython import embed; embed()
    if user_form.validate():
        new_user = Users(
            email=request.form.get("email"),
            name=request.form.get("name"),
            password=generate_password_hash(request.form.get("password"), method='sha256')
        )

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    else:
        return render_template("signup.html", form=user_form)

# Routes for handling user specific pages
@users.route("/users/<int:user_id>")
@login_required
def profile(user_id):
    if current_user.id != user_id:
        logger.warning("wrong user.id and current_user.id")
        return render_template("home.html")

    return render_template("user.html")


@users.route("/users/<int:user_id>/edit")
@login_required
def edit(user_id):
    return "Sorry, the page was not implemneted yet!"
