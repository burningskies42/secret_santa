from loguru import logger
from flask import Blueprint, render_template, request
from flask_login import login_required

from secret_santa.utils import assign_all_santas, assign_santa_to_target
from secret_santa import db


# start application definitions
groups = Blueprint(
    "groups",
    __name__,
    template_folder="templates"
)


@groups.route("/groups/create/user/<int:user_id>")
@login_required
def create(user_id):
    return "Sorry, the page was not implemneted yet!"

@groups.route("/groups/create/user/<int:user_id>", methods=["POST"])
@login_required
def create_post(user_id):
    return "Sorry, the page was not implemneted yet!"


@groups.route("/groups/<int:group_id>/join/user/<int:user_id>")
@login_required
def join(user_id):
    return "Sorry, the page was not implemneted yet!"


@groups.route("/groups/<int:group_id>/draw/user/<int:user_id>")
@login_required
def draw_name(group_id, user_id):
    return "Sorry, the page was not implemneted yet!"


@groups.route("/groups/<int:group_id>/draw_init")
@login_required
def draw_init(group_id):
    return "Sorry, the page was not implemneted yet!"
