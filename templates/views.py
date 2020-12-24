from loguru import logger

from flask import Blueprint, make_response, redirect, render_template, request, url_for, flash
from secret_santa import db

# start application definitions
main = Blueprint(
    'main',
    __name__
)


# define routes
@main.route("/", methods=["POST", "GET"])
def index():
    return render_template("home.html", title="Welcome to BestSecret Santa!")
