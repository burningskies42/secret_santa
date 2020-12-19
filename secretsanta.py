from loguru import logger

from flask import Blueprint, make_response, redirect, render_template, request, url_for, flash
from . import db

# start application definitions
main = Blueprint('main', __name__)


# define routes
@main.route("/", methods=["POST", "GET"])
def index():
    return render_template("home.html")


# Testing to check if it works
@main.route("/test", methods=["GET", "POST"])
def test():
    logger.debug(f"auth: {request.authorization}")
    return "Works!"


# Redirect all non existent URLsto index.html
@main.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))
