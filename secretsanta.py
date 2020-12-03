import argparse
import os
import random

from flask import Flask, redirect, render_template, request, url_for
from loguru import logger
from waitress import serve

from utils import add_user, assign_all_santas, assign_santa_to_target, enable_draw, get_all_users, get_free_santas, get_user_addresses, login_user

# start application definitions
draw_phase = "ENABLE_DRAW" in os.environ.keys()
user_login = None
app = Flask(__name__)


# define routes
@app.route("/", methods=["POST", "GET"])
def index():
    if "go_to_submit" in request.form:
        return redirect(url_for("submit_address"))

    if "go_to_login" in request.form:
        return redirect(url_for("login"))

    if "go_to_draw" in request.form:
        return redirect(url_for("draw_name"))
    logger.debug(f"enable button {enable_draw(draw_phase)}")
    return render_template("home.html", disable_draw=enable_draw(draw_phase))


# Route for handling the login page logic
@app.route("/login", methods=["GET", "POST"])
def login():
    response = None
    if request.method == "POST":
        logged_user = dict(request.form)["user_login"]
        logger.debug(f"{logged_user} logged in")
        assign_all_santas()
        response = login_user(request.form["user_login"], request.form["user_password"])
        if response != 0:
            render_template("login.html", error=response)
        else:
            user_login = request.form["user_login"]
            response = f"You are now logged in as {user_login}"
            target_name, target_address = assign_santa_to_target(user_login)
            return f"You have drawn {target_name}.<br>Posting Address is:<br>{target_address}"
            # return render_template("home.html", message=response)

    return render_template("login.html", error=response)


@app.route("/submit", methods=["GET", "POST"])
def submit_address():
    error = None

    if request.method == "POST":
        error = add_user(request.form)
        if error is not None:
            return render_template("address_form.html", error=error)

        processed_text = f"Thank you {request.form['name'].title()}!\n your data has been submitted"
        return render_template("home.html", message=processed_text, disable_draw=enable_draw(draw_phase))

    elif request.method == "GET":
        return render_template("address_form.html")


@app.route("/addresses", methods=["GET"])
def show_tables():
    return get_user_addresses().to_html()


@app.route("/draw",)
def draw_name():
    # if request.method == "GET":
    #     name_list = get_free_santas().values.tolist()
    #     name_list = [{"id": uid, "val": uname} for uid, uname in name_list]
    #     return render_template("draw_name.html", name_list=name_list)

    # if request.method == "POST":
    # santa_id = request.form["name_selection"]
    target_name, target_address = assign_santa_to_target(user_login)
    return f"You have drawn {target_name}.<br>Posting Address is:<br>{target_address}"


# Testing to check if it works
@app.route("/test")
def test():
    return "Works!"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--port", help="port to run on", default="5000")
    parser.add_argument("-D", "--debug", help="run in debug mode", action="store_true")
    args = parser.parse_args()

    PORT = args.port or os.getenv("PORT") or "5000"

    if args.debug:
        app.run(port=PORT, debug=True)
    else:
        serve(app, host="0.0.0.0", port=PORT)
