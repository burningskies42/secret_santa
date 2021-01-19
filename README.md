# BestSecret-Santa
### Simple tool for creating a raffle of users

- In the first phase participants will enter their data
- After the collection phase, users can draw from the pool and get assigned a (best)secret-santa at random


## Setup

The best way to run the app is to export the FLASK_APP environment where the __init__.py file is located. Next start the app by calling `flask app`. Flask supported argumenets can be used to configure your Flask app (e.g --port). E.g.:

> FLASK_APP=~/Documents/secret_santa python -m flask run --port=1337

In case you want to use Flask debug mode set the FLASK_ENV to development. In case you want to reset the database set the RESET_DB env to `1` and run:

> FLASK_APP=~/Documents/secret_santa FLASK_ENV=development RESET_DB=1 python -m flask run

Before launching the app you must have a CSRF key saved as an environment variable (or pass it together in the same line). The variable has to be saved in SECRET_KEY. Easiest way to do this if you are using a virtual environment is so add such a command to the venv start-up script:
> echo "export SECRET_KEY=super_secret_key" >> venv/bin/activate
