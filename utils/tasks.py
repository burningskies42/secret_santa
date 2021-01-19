from datetime import datetime, timedelta
from random import randrange

from loguru import logger

from secret_santa import db
from secret_santa.models import Group, Member, Santa


def get_ts(offset=0):
    return datetime.now() + timedelta(minutes=offset)


def assign_all_santas(group_id):
    found_members = Member.query.filter_by(group_id=group_id).all()
    member_ids = [memb.user_id for memb in found_members]
    santa_ids = sattolo_cycle(member_ids)
    logger.debug(f"assignments: {[member_ids, santa_ids]}")

    for member_id, santa_id in zip(member_ids, santa_ids):
        db.session.add(Santa(group_id=group_id, presentee_id=member_id, santa_id=santa_id))

    found_group = Group.query.get(group_id)
    found_group.is_raffled = True

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


def delete_group(group):
    db.session.delete(group)
    for member in Member.query.filter_by(group_id=group.id).all():
        db.session.delete(member)
    for santa in Santa.query.filter_by(group_id=group.id).all():
        db.session.delete(santa)

    db.session.commit()
