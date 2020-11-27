import datetime
import random

import pandas as pd
from loguru import logger

from .db import Connection


def get_ts():
    return datetime.datetime.now()


def get_user_addresses():
    query = open("sqls/user_addresses.sql", "r").read()
    with Connection("santa.db") as conn:
        return conn.query_dataframe(query)


def get_free_santas():
    query = open("sqls/free_santas.sql", "r").read()
    with Connection("santa.db") as conn:
        return conn.query_dataframe(query)


def get_free_targets():
    query = open("sqls/free_targets.sql", "r").read()
    with Connection("santa.db") as conn:
        return conn.query_dataframe(query).set_index("user_id")


def add_user(name, address):
    with Connection("santa.db") as conn:
        user_id = conn.query("SELECT MAX(USER_ID) LAST_USER FROM USERS")[0]["LAST_USER"]
        user_id += 1
        logger.debug(f"new user_id is: {user_id}")

        # add user to table
        add_user_query = open("sqls/add_user.sql", "r").read()
        conn.execute(add_user_query, (user_id, name, get_ts(),))

        # add address to table
        add_address_query = open("sqls/add_address.sql", "r").read()
        conn.execute(add_address_query, (user_id, address, get_ts(),))


def assign_santa_to_target(santa_id):
    santa_id = int(santa_id)

    # supressing errors incase only one user remains
    addresses_df = get_free_targets().drop(santa_id, errors="ignore")
    logger.info(f"User {int(santa_id)} excluded from selection")
    target_id, target_name, target_address = addresses_df.reset_index().sample(1).iloc[0].values
    target_id = int(target_id)
    logger.info(f"{target_id} was randomly drawn")

    query = open("sqls/assign_santa.sql", "r").read()
    with Connection("santa.db") as conn:
        conn.execute(query, (santa_id, target_id, get_ts(),))

    return target_name, target_address
