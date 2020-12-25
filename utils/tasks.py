from datetime import datetime, timedelta
from random import randrange

from loguru import logger
from secret_santa import db
from secret_santa.models import Member, Santa

#TODO: remove unneeded imports and functionality
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


def assign_all_santas(group_id):
    found_members = Member.query.filter_by(group_id=group_id).all()
    member_ids = [memb.user_id for memb in found_members]
    santa_ids = sattolo_cycle(member_ids)
    logger.debug(f"assignments: {[member_ids, santa_ids]}")

    for member_id, santa_id in zip(member_ids, santa_ids):
        db.session.add(Santa(group_id=group_id, presentee_id=member_id, santa_id=santa_id))
    db.session.commit()


def sattolo_cycle(items):
    """Sattolo's algorithm."""
    new_items = items.copy()
    i = len(new_items)
    while i > 1:
        i = i - 1
        j = randrange(i)  # 0 <= j <= i-1
        new_items[j], new_items[i] = new_items[i], new_items[j]

    return new_items
