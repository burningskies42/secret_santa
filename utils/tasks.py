import datetime
import random

import pandas as pd
from loguru import logger
from werkzeug.security import check_password_hash, generate_password_hash

from .db import Connection


def enable_draw(enable):
    if enable:
        return ""
    else:
        return "disabled"


def get_ts():
    return datetime.datetime.now()


def get_user_addresses():
    query = open("sqls/user_addresses.sql", "r").read()
    with Connection("santa.db") as conn:
        return conn.query_dataframe(query)


def get_all_users():
    query = open("sqls/all_users.sql", "r").read()
    with Connection("santa.db") as conn:
        return conn.query_dataframe(query)


def get_free_santas():
    query = open("sqls/free_santas.sql", "r").read()
    with Connection("santa.db") as conn:
        return conn.query_dataframe(query)


def get_free_targets(exclude_id):
    query = open("sqls/free_targets.sql", "r").read()
    with Connection("santa.db") as conn:
        return conn.query_dataframe(query, (exclude_id, exclude_id,)).set_index("USER_ID")


def assign_santa_to_target(user_login):
    santa_id = None
    with Connection("santa.db") as conn:
        query = f"SELECT USER_ID FROM USERS WHERE USER_LOGIN = '{user_login}'"
        logger.debug(query)
        santa_id = conn.query(query)[0]["USER_ID"]

    logger.debug(f"user_id {santa_id} returned from DB")

    # supressing errors incase only one user remains
    try:
        addresses_df = get_free_targets(santa_id)
    except Exception as e:
        return e

    logger.info(f"User {int(santa_id)} excluded from selection")
    target_id, target_name, target_address = addresses_df.reset_index().sample(1).iloc[0].values
    target_id = int(target_id)
    logger.info(f"{target_id} was randomly drawn")

    query = open("sqls/assign_santa.sql", "r").read()
    with Connection("santa.db") as conn:
        conn.execute(query, (santa_id, target_id, get_ts(),))

    return target_name, target_address
