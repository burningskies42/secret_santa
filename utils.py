import pandas as pd
from loguru import logger

from db import Connection


def get_user_addresses():
    query = open("sqls/user_addresses.sql", "r").read()
    with Connection("santa.db") as conn:
        return conn.query_dataframe(query)


def add_user(name, address):
    with Connection("santa.db") as conn:
        user_id = conn.query("SELECT MAX(USER_ID) LAST_USER FROM USERS")[0]["LAST_USER"]
        user_id += 1
        logger.debug(user_id)

        conn.execute("INSERT INTO USERS(USER_ID, USER_NAME) VALUES (?, ?)", (user_id, name,))

        conn.execute("INSERT INTO ADDRESSES(USER_ID, USER_ADDRESS) VALUES (?, ?)", (user_id, address,))
