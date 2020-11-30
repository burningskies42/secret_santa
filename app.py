import os
import random

from flask import Flask, redirect, render_template, request, url_for
from loguru import logger

from utils import add_user, assign_santa_to_target, get_all_users, get_free_santas, get_user_addresses

# start application definitions
PORT = os.getenv("PORT")
disable_draw = "disabled" if "ENABLE_DRAW" not in os.environ.keys() else ""

app = Flask(__name__)


# define routes
@app.route("/", methods=["POST", "GET"])
def index():
    if "go_to_submit" in request.form:
        return redirect(url_for("submit_address"))

    if "go_to_draw" in request.form:
        return redirect(url_for("draw_name"))

    logger.debug(request.form)
    return render_template("home.html", disable_draw=disable_draw)

@app.route("/submit", methods=["GET", "POST"])
def submit_address():
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        add_user(name, address)
        processed_text = f"Thank you {name.title()}!<br>\n your data has been submitted"
        return processed_text

    elif request.method == "GET":
        return render_template("address_form.html")

@app.route("/addresses", methods=["GET"])
def show_tables():
    return get_user_addresses().to_html()


@app.route("/draw", methods=["GET", "POST"])
def draw_name():
    if request.method == "GET":
        name_list = get_all_users().values.tolist()
        name_list = [{"id": uid, "val": uname} for uid, uname in name_list]
        return render_template("draw_name.html", name_list=name_list)

    elif request.method == "POST":
        santa_id = request.form["name_selection"]
        target_name, target_address = assign_santa_to_target(santa_id)
        return f"You have drawn {target_name}.<br>Posting Address is:<br>{target_address}"

#Testing to check if it works
@app.route('/test')
def test():
    return "Works!"

if __name__ == '__main__':
    app.run(port=PORT, debug=True)
