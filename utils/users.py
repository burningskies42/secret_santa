import sys

from loguru import logger
from werkzeug.security import check_password_hash, generate_password_hash

from .db import Connection
from .tasks import get_ts


def add_user(request_form):
    necessary_fields = {"name", "address", "login", "password"}

    name = request_form["name"]
    address = request_form["address"]
    login = request_form["login"]
    password = request_form["password"]
    if len(password) < 8:
        return "Password must have at least 8 characters"

    # validate no empty field
    missing_fields = necessary_fields - set([k for k, v in request_form.items() if len(v) > 0])
    logger.debug(f"missing fields: {request_form}")
    if len(missing_fields) > 0:
        return f"Field {str.upper(list(missing_fields)[0])} cannot be empty"

    # validate user name not in DB
    with Connection("santa.db") as conn:
        user_id = conn.query("SELECT MAX(USER_ID) LAST_USER FROM USERS")[0]["LAST_USER"] or 0
        user_id += 1

        error = check_valid_user(login)
        if error is not None:
            return error

        # add user to table
        add_user_query = open("sqls/add_user.sql", "r").read()
        conn.execute(add_user_query, (user_id, name, login, generate_password_hash(password), get_ts(),))

        # add address to table
        add_address_query = open("sqls/add_address.sql", "r").read()
        try:
            conn.execute(add_address_query, (user_id, address, get_ts(),))
        except Exception as e:
            logger.error(e)
            conn.rollback()
            return e


def check_valid_user(login):
    with Connection("santa.db") as conn:
        user_id = conn.query("SELECT user_id FROM USERS WHERE USER_LOGIN = ?", (login,))
        logger.debug(f"checking if user {login} is already in db: {user_id}")
        if len(user_id) > 0:
            return f"cannot add {login}. Login already found in DB"
        else:
            return None


def login_user(user_login, user_password):
    with Connection("santa.db") as conn:
        response = conn.query("SELECT USER_PASSWORD_HASH FROM USERS WHERE USER_LOGIN = ?", (user_login,))
        if len(response) == 0 or "USER_PASSWORD_HASH" not in response[0].keys():
            logger.info(f"cannot find user {user_login}")
            return f"cannot find user {user_login}"
        elif not check_password_hash(response[0]["USER_PASSWORD_HASH"], user_password):
            logger.info(f"wrong password for user {user_login}")
            return f"wrong password for user {user_login}"
        else:
            logger.info(f"{user_login} successfully logged in")
            return 0
