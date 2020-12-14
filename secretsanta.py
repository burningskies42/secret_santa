from loguru import logger

from flask import Blueprint, make_response, redirect, render_template, request, url_for, flash
from utils import (
    add_user,
    assign_all_santas,
    assign_santa_to_target,
    enable_draw,
    get_user_addresses,
    login_user
)

# start application definitions
main = Blueprint('main', __name__)


# define routes
@main.route("/", methods=["POST", "GET"])
def index():
    return render_template("home.html")

@main.route("/draw")
def draw_name():
    target_name, target_address = assign_santa_to_target(request.cookies.get("user_login"))

    if target_name:
        return render_template(
            "address_drawn.html",
            target_name=target_name,
            target_address=target_address,
            user=request.cookies.get("user_login") or "LOGIN"
        )

    return "Sorry, there was no assignment yet!"


@main.route("/draw_init")
def draw_init():
    assign_all_santas()
    return render_template(
        "home.html",
        message="Raffled names",
        user=request.cookies.get("user_login") or "LOGIN"
    )


# Testing to check if it works
@main.route("/test", methods=["GET", "POST"])
def test():
    logger.debug(f"auth: {request.authorization}")
    return "Works!"


# Redirect all non existent URLsto index.html
@main.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))
