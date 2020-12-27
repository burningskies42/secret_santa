from flask import Blueprint, flash, make_response, redirect, render_template, request, url_for
from loguru import logger

from secret_santa_app import db

# start application definitions
main = Blueprint("main", __name__)


# define routes
@main.route("/", methods=["POST", "GET"])
def index():
    return render_template("home.html", title="Welcome to BestSecret Santa!")
