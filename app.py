import os
import random

from flask import Flask, redirect, render_template, request, url_for

from utils import add_to_table, read_address_table

# start application definitions
PORT = os.getenv("PORT")
app = Flask(__name__)


# define routes
@app.route("/", methods=["POST", "GET"])
def index():
    if "go_to_submit" in request.form:
        return redirect(url_for("submit_address"))

    return render_template("home.html")


@app.route("/submit", methods=["GET", "POST"])
def submit_address():
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        add_to_table(name, address)
        processed_text = f"Thank you {name.title()}!<br>\n your data has been submitted"
        return processed_text

    elif request.method == "GET":
        return render_template("address_form.html")


@app.route("/addresses", methods=["GET"])
def show_tables():
    return read_address_table().to_html()


@app.route("/draw", methods=["GET", "POST"])
def draw_name():
    if request.method == "GET":
        name_list = read_address_table()["Name"].values.tolist()
        name_list = [{"id": i, "val": v} for i, v in enumerate(name_list)]
        return render_template("draw_name.html", name_list=name_list)

    elif request.method == "POST":
        user_id = request.form["name_selection"]
        addresses_df = read_address_table().drop(int(user_id))
        print(f"User {int(user_id)} excluded from selction")

        target = random.choice(addresses_df.index.values)
        print(f"{target} was randomly drawn")
        print(addresses_df.to_string())
        target_data = addresses_df.loc[target]

        return f"You have drawn {target_data['Name']}.<br>Posting Address is:<br>{target_data['Address']}"


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
