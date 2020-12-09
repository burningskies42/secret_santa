import random
import string

from loguru import logger
from werkzeug.security import check_password_hash, generate_password_hash

from functools import wraps
from flask import request, Response

from .db import Connection
from .tasks import get_ts


def login_attempts_for_ip(ip_address, minutes):
    with Connection("santa.db") as conn:
        last_minutes = f"-{minutes} minutes"
        ret = conn.query(
            "select count(*) CNT from logins where ip_address = ? and createdts >= datetime('now', ?)",
            (ip_address, last_minutes, )
        )[0]["CNT"]

    return ret


def log_login_attempt(ip_address, login_name):
    with Connection("santa.db") as conn:
        conn.execute(
            "INSERT INTO logins(ip_address, login, createdts) VALUES (?, ?, ?)",
            (ip_address, login_name, get_ts(),)
        )

def add_user(request_form):
    necessary_fields = {"name", "address", "login", "password"}

    name = request_form["name"]
    address = request_form["address"]
    login = request_form["login"]
    password = request_form["password"]

    if len(password) < 8:
        return "Password must have at least 8 characters"

    recieved_data = set(request_form.keys())

    # validate no empty field
    missing_fields = necessary_fields - recieved_data
    logger.debug(f"missing fields: {missing_fields}")
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
        is_admin = True if user_id == 1 else False
        conn.execute(add_user_query, (user_id, name, login, generate_password_hash(password), get_ts(), is_admin,))

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


def login_user(user_login, user_password, request_ip):
    with Connection("santa.db") as conn:
        response = conn.query("SELECT USER_LOGIN, USER_PASSWORD_HASH, IS_ADMIN FROM USERS WHERE USER_LOGIN = ?", (user_login,))
        cookies = {}
        log_login_attempt(request_ip, user_login)
        login_attempts = login_attempts_for_ip(request_ip, 5)
        logger.debug(f"{login_attempts} login attempts from ip {request_ip} in last 5 minutes")

        if login_attempts >= 5:
            result = "too many attempts from this ip: blacklisting"
            logger.info(result)
        elif len(response) == 0 or "USER_PASSWORD_HASH" not in response[0].keys():
            result = "wrong combination or user and password"
            logger.info(result)
        elif not check_password_hash(response[0]["USER_PASSWORD_HASH"], user_password):
            result = "wrong combination or user and password"
            logger.info(result)
        else:
            result = f"{user_login} successfully logged in"
            logger.info(result)

            letters_and_digits = string.ascii_letters + string.digits
            hashed = "".join((random.choice(letters_and_digits) for i in range(64)))
            conn.query("UPDATE users SET COOKIE = ?, COOKIE_VALID_TO = ? WHERE USER_LOGIN = ?", (hashed, get_ts(offset=60), user_login,))
            conn.commit()

            cookies["user_cookie"] = hashed
            cookies["admin_cookie"] = response[0]["IS_ADMIN"]
            cookies["user_login"] = response[0]["USER_LOGIN"]

        return result, cookies

def check_auth(username, password, remote_addr):
    """This function is called to check if a username /
    password combination is valid.
    """
    msg, cookies = login_user(username, password, remote_addr)
    logger.debug(cookies)
    check = ("successfully logged in" in msg ) and (cookies["admin_cookie"] == 1)
    return check

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password, request.remote_addr):
            return authenticate()
        return f(*args, **kwargs)
    return decorated