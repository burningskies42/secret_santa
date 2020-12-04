from datetime import datetime, timedelta
import random
from random import randrange

import pandas as pd
from loguru import logger
from werkzeug.security import check_password_hash, generate_password_hash

from .db import Connection


def enable_draw(enable):
    if enable:
        return ""
    else:
        return "disabled"


def get_ts(offset=0):
    return datetime.now() + timedelta(minutes=offset)


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
    with Connection("santa.db") as conn:
        query = open("sqls/get_target.sql", "r").read()
        resp = conn.query(query, (user_login,))
        logger.debug(resp)

        if len(resp) > 0:
            return resp[0]["USER_NAME"], resp[0]["USER_ADDRESS"]

        return None, None


def assign_all_santas():
    query = "INSERT INTO SANTAS(SANTA_ID, TARGET_ID, CREATEDTS) VALUES(?, ?, current_timestamp)"

    with Connection("santa.db") as conn:
        entries_in_santas = conn.query("SELECT COUNT(*) CNT FROM SANTAS")[0]["CNT"]
        logger.debug(f"entries_in_santas: {entries_in_santas}")
        entries_in_users = conn.query("SELECT COUNT(*) CNT FROM USERS")[0]["CNT"]
        logger.debug(f"entries_in_users: {entries_in_users}")

        if entries_in_santas < entries_in_users:
            users = [d["USER_ID"] for d in conn.query("SELECT USER_ID FROM USERS")]
            santas = sattolo_cycle(users)
            logger.debug([santas, users])
            [conn.execute(query, (s, u,)) for s, u in zip(santas, users)]
        else:
            logger.debug("Already assigned santas")


def sattolo_cycle(items):
    """Sattolo's algorithm."""
    new_items = items.copy()
    i = len(new_items)
    while i > 1:
        i = i - 1
        j = randrange(i)  # 0 <= j <= i-1
        new_items[j], new_items[i] = new_items[i], new_items[j]
    return new_items


def reset_database():
    sql_files = [
        "drop_tables.sql",
        "create_table_users.sql",
        "create_table_santas.sql",
        "create_table_addresses.sql"
    ]

    with Connection("santa.db") as conn:
        for sql in sql_files:
            with open(f"sqls/{sql}", "r") as f:
                for query in f.read().split(";"):
                    conn.query(query)
                logger.debug(f"'{sql}' executed")

    return True
