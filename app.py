from flask import Flask, request, render_template, url_for, redirect
import pandas as pd
import random
from utils import read_address_table, add_to_table

PORT = 1337

### start application definitions
app = Flask(__name__)

# define routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if "go_to_submit" in request.form:
        return redirect(url_for('submit_address'))

    return render_template('home.html')

@app.route('/submit', methods=["GET"])
def submit_address():
    return render_template('submit_form.html')


@app.route('/submit', methods=['POST'])
def confirm_submission():
    name = request.form['name']
    is_success = add_to_table(name, request.form['address'])

    return render_template("submit_success.html", is_success=is_success, name=name.title())

@app.route('/addresses')
def show_tables():
    return read_address_table().to_html()


@app.route("/draw")
def draw_name():
    name_list = read_address_table()["Name"].values.tolist()
    name_list = [{"id": i, "val": v} for i,v in enumerate(name_list)]

    return render_template('names.html', name_list=name_list)

@app.route("/draw", methods=['POST'])
def select_name():

    user_id = request.form["name_selection"]
    addresses_df = read_address_table().drop(int(user_id))
    print(f"User {int(user_id)} excluded from seelction")

    target = random.choice(addresses_df.index.values)
    print(f"{target} was randomly drawn")
    print(addresses_df.to_string())
    target_data = addresses_df.loc[target]

    return f"You have drawn {target_data['Name']}.<br>Posting Address is:<br>{target_data['Address']}"


if __name__ == '__main__':
    app.run(port=PORT, debug=True)
