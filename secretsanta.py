import argparse
import os

from flask import Flask, make_response, redirect, render_template, request, url_for, flash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_ipban import IpBan

from loguru import logger
from waitress import serve

from utils import add_user, assign_all_santas, assign_santa_to_target, enable_draw, get_user_addresses, login_user, reset_database, requires_auth

# start application definitions
user_login = None
app = Flask(__name__)
app.secret_key = os.urandom(24)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
ip_ban = IpBan(ban_seconds=200)
ip_ban.init_app(app)

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
        "home.html",
        disable_draw=enable_draw(cookie_hash is not None),
        disable_draw_admin=enable_draw(cookie_hash is not None and str(cookie_admin) == "1"),
        user=request.cookies.get("user_login") or "LOGIN",
    )


# Route for handling the login page logic
@app.route("/login", methods=["GET", "POST"])
# @limiter.limit("100/day;10/hour;3/minute")
def login():
    response = None
    if request.method == "POST":
        logged_user = dict(request.form)["user_login"]
        logger.debug(f"requst with user-name {logged_user} from ip {request.remote_addr}")
        response, set_cookies = login_user(request.form["user_login"], request.form["user_password"], request.remote_addr)
        if "successfully logged in" not in response:
            if "too many attempts from this ip" in response:
                ip_ban.add()
                return 'Go away grinch, you are blacklisted'
            else:
                return render_template("login.html", error=response, user=request.cookies.get("user_login") or "LOGIN")

        logger.debug(f"set_cookies: {set_cookies}")

        resp = make_response(redirect(url_for("index")))
        for key in set_cookies.keys():
            resp.set_cookie(key, str(set_cookies[key]))

        return resp

    return render_template("login.html", error=response, user=request.cookies.get("user_login") or "LOGIN")


@app.route("/submit", methods=["GET", "POST"])
@limiter.limit("100/day;20/hour;10/minute")
def submit_address():
    error = None

    if request.method == "POST":
        error = add_user(request.form)
        if error is not None:
            return render_template("submit_form.html", error=error, user=request.cookies.get("user_login") or "LOGIN")

        processed_text = f"Thank you {request.form['name'].title()}!\n your data has been submitted"
        return render_template("home.html", message=processed_text, user=request.cookies.get("user_login") or "LOGIN")

    elif request.method == "GET":
        return render_template("submit_form.html", user=request.cookies.get("user_login") or "LOGIN")


@app.route("/draw")
def draw_name():

    target_name, target_address = assign_santa_to_target(request.cookies.get("user_login"))

    if target_name:
        return render_template("address_drawn.html", target_name=target_name, target_address=target_address, user=request.cookies.get("user_login") or "LOGIN")

    return "Sorry, there was no assignment yet!"


@app.route("/draw_init")
@requires_auth
def draw_init():
    assign_all_santas()
    return render_template("home.html", message="Raffled names", user=request.cookies.get("user_login") or "LOGIN")

# Testing to check if it works
@app.route("/test", methods=["GET", "POST"])
def test():
    logger.debug(f"auth: {request.authorization}")
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
