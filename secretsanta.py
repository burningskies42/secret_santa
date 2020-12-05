import argparse
import os
import random

from flask import Flask, make_response, redirect, render_template, request, url_for
from loguru import logger
from waitress import serve

from utils import add_user, assign_all_santas, assign_santa_to_target, enable_draw, get_user_addresses, login_user, reset_database

# start application definitions
user_login = None
app = Flask(__name__)


# define routes
@app.route("/", methods=["POST", "GET"])
def index():
    cookie_hash = request.cookies.get("user_cookie")
    cookie_admin = request.cookies.get("admin_cookie")

    if "go_to_submit" in request.form:
        return redirect(url_for("submit_address"))

    if "go_to_login" in request.form:
        return redirect(url_for("login"))

    if "go_to_draw" in request.form:
        return redirect(url_for("draw_name"))

    if "go_to_draw_init" in request.form:
        return redirect(url_for("draw_init"))

    return render_template(
        "home.html", disable_draw=enable_draw(cookie_hash is not None), disable_draw_admin=enable_draw(cookie_hash is not None and str(cookie_admin) == "1")
    )


# Route for handling the login page logic
@app.route("/login", methods=["GET", "POST"])
def login():
    response = None
    if request.method == "POST":
        logged_user = dict(request.form)["user_login"]
        logger.debug(f"{logged_user} logged in")
        response, set_cookies = login_user(request.form["user_login"], request.form["user_password"])
        logger.debug(f"set_cookies: {set_cookies}")

        resp = make_response(redirect(url_for("index")))
        for key in set_cookies.keys():
            resp.set_cookie(key, str(set_cookies[key]))

        return resp

    return render_template("login.html", error=response)


@app.route("/submit", methods=["GET", "POST"])
def submit_address():
    error = None

    if request.method == "POST":
        error = add_user(request.form)
        if error is not None:
            return render_template("submit_form.html", error=error)

        processed_text = f"Thank you {request.form['name'].title()}!\n your data has been submitted"
        return render_template("home.html", message=processed_text)

    elif request.method == "GET":
        return render_template("submit_form.html")


@app.route("/addresses", methods=["GET"])
def show_tables():
    df = get_user_addresses()
    if df.empty:
        return "Draw not yet initialized!"

    return render_template("get_addresses.html", tables=[df.to_html(classes="data")], titles=df.columns.values)


@app.route("/draw")
def draw_name():
    user_login = request.cookies.get("user_login")
    target_name, target_address = assign_santa_to_target(user_login)

    if target_name:
        return render_template("address_drawn.html", user=user_login, target_name=target_name, target_address=target_address)

    return "Sorry, there was no assignment yet!"


@app.route("/draw_init")
def draw_init():
    assign_all_santas()
    return render_template("home.html", message="Raffled names")


# Testing to check if it works
@app.route("/test")
def test():
    return "Works!"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--port", help="port to run on", default="5000")
    parser.add_argument("-D", "--debug", help="run in debug mode", action="store_true")
    parser.add_argument("-R", "--resetdb", help="reset database", action="store_true")
    args = parser.parse_args()

    PORT = args.port or os.getenv("PORT") or "5000"

    if args.resetdb:
        logger.debug("Start DB reset")
        reset_database()

    if args.debug:
        app.run(port=PORT, debug=True)
    else:
        serve(app, host="0.0.0.0", port=PORT)
