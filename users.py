from loguru import logger
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from . import db


users = Blueprint("users", __name__)

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
