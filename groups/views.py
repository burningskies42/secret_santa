from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from loguru import logger

from secret_santa import db
from secret_santa.models import Group, User, Member, Santa
from secret_santa.groups.forms import GroupCreateForm, GroupDeleteForm
from secret_santa.models import Group, Member, User, Santa
from secret_santa.utils import assign_all_santas


# start application definitions
groups = Blueprint("groups", __name__, template_folder="templates")


@groups.route("/")
def index():
    groups = []
    for group in Group.query.all():
        owner = User.query.filter_by(id=group.owner_id).first()
        groups.append((group, owner.name))

    return render_template("groups/index.html", title="Groups", groups=groups)


@groups.route("/create")
@login_required
def create():
    group_form = GroupCreateForm()
    return render_template("groups/create.html", form=group_form)


@groups.route("/create", methods=["POST"])
@login_required
def create_post():
    logger.debug(request.form)
    group = Group.query.filter_by(name=request.form.get("name")).first()
    if group:
        flash("Group name is already in use.", "is-warning")
        return redirect(url_for("groups.create"))

    group_form = GroupCreateForm(request.form)
    if group_form.validate():
        db.session.add(Group(name=request.form.get("name"), owner_id=current_user.id))
        group = Group.query.filter_by(name=request.form.get("name")).first()
        db.session.add(Member(group_id=group.id, user_id=current_user.id, is_owner=True))
        db.session.commit()

        flash("Successfully created Group!", "is-success")
        return redirect(url_for("groups.index"))

    flash("Couldn't create group. Please check the inputs!", "is-warning")
    return render_template("groups/create.html", form=group_form)


@groups.route("/<int:group_id>/delete")
@login_required
def delete(group_id):
    found_group = Group.query.get(group_id)
    if found_group and current_user.id == found_group.owner_id:
        db.session.delete(found_group)
        found_members = Member.query.filter_by(group_id=group_id).all()
        for member in found_members:
            db.session.delete(member)
        db.session.commit()

        flash(f"Group <{group_id}> successfully deleted!", "is-success")
        return redirect(url_for("groups.index"))

    flash(f"Could not delete Group <{group_id}>!", "is-warning")
    return redirect(url_for('groups.profile', group_id=group_id))


@groups.route("/<int:group_id>/profile")
def profile(group_id):
    found_group = Group.query.get(group_id)
    if not found_group:
        flash("Could not find Group!", "is-warning")
        redirect(url_for("groups.index"))

    users = ( Member
        .query
        .filter_by(group_id=group_id)
        .join(User, Member.user_id == User.id)
        .add_columns(User.id, User.name)
        .all()
    )

    presentees = ( Member
        .query
        .join(Santa, Member.user_id == Santa.santa_id, isouter=True)
        .filter_by(group_id=group_id)
        .join(User, Santa.santa_id == User.id, isouter=True)
        .add_columns(User.id, User.name)
        .all()
    )

    presentees = presentees or [None] * len(users)
    logger.debug(f"users: {users}")
    logger.debug(f"presentees: {presentees}")

    return render_template("groups/profile.html", group=found_group, users=zip(users, presentees))


@groups.route("/<int:group_id>/join")
@login_required
def join(group_id):
    found_group = Group.query.get(group_id)
    if not found_group:
        flash("Could not find group!", "is-warning")
        return redirect(url_for("groups.index"))

    if Member.query.filter_by(group_id=group_id, user_id=current_user.id).first():
        flash("You are already a member of this group!", "is-warning")
        return redirect(url_for("groups.profile", group_id=group_id))

    db.session.add(Member(group_id=found_group.id, user_id=current_user.id, is_owner=False))
    db.session.commit()

    flash("Successfully joined group!", "is-success")
    return redirect(url_for("groups.profile", group_id=group_id))


@groups.route("/<int:group_id>/leave")
@login_required
def leave(group_id):
    found_group = Group.query.get(group_id)
    logger.warning(f"group: {found_group}")
    member = Member.query.filter_by(group_id=group_id, user_id=current_user.id).first()
    if found_group and member:
        db.session.delete(member)
        db.session.commit()

        flash(f"Left Group <{group_id}> successfully!", "is-success")
        return redirect(url_for('groups.profile', group_id=group_id))

    flash(f"Could not remove User <{current_user.id}> from Group <{group_id}>!", "is-warning")
    return redirect(url_for('groups.profile', group_id=group_id))


@groups.route("/<int:group_id>/kick/<int:user_id>")
@login_required
def kick(group_id, user_id):
    found_group = Group.query.get(group_id)
    logger.warning(f"group: {found_group}")
    member = Member.query.filter_by(group_id=group_id, user_id=user_id).first()
    if found_group and member:
        db.session.delete(member)
        db.session.commit()

        flash(f"User <{user_id}> was kicked from Group <{group_id}>!", "is-success")
        return redirect(url_for('groups.profile', group_id=group_id))

    flash(f"Could not remove User <{user_id}> from Group <{group_id}>!", "is-warning")
    return redirect(url_for('groups.profile', group_id=group_id))


@groups.route("/<int:group_id>/raffle")
@login_required
def raffle(group_id):
    found_group = Group.query.filter_by(id=group_id, owner_id=current_user.id).first()
    if found_group and found_group.is_raffled:
        flash("Already raffled members!", "is-success")
        return redirect(url_for('groups.profile', group_id=group_id))

    if found_group:
        assign_all_santas(found_group.id)
        flash("Succesfully raffled members!", "is-success")
        return redirect(url_for('groups.profile', group_id=group_id))

    flash("Could not initiate raffle!", "is-warning")
    return redirect(url_for('groups.profile', group_id=group_id))


@groups.route("/<int:group_id>/draw")
@login_required
def draw_name(group_id):
    return "Sorry, the page was not implemneted yet!"
