from loguru import logger
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from secret_santa.utils import assign_all_santas, assign_santa_to_target

from secret_santa import db
from secret_santa.models import Groups, Users, Members
from secret_santa.groups.forms import GroupForm, DeleteForm


# start application definitions
groups = Blueprint(
    "groups",
    __name__,
    template_folder="templates"
)


@groups.route("/")
def index():
    groups = []
    for group in Groups.query.all():
        owner = Users.query.filter_by(id=group.owner_id).first()
        groups.append((group, owner.name))

    return render_template("groups/index.html", title="Groups", groups=groups)


@groups.route("/create")
@login_required
def create():
    group_form = GroupForm()
    return render_template("groups/create.html", form=group_form)

@groups.route("/create", methods=["POST"])
@login_required
def create_post():
    logger.debug(request.form)
    group = Groups.query.filter_by(name=request.form.get("name")).first()
    if group:
        flash("Group name is already in use.", "is-warning")
        return redirect(url_for('groups.create'))

    group_form = GroupForm(request.form)
    if group_form.validate():
        db.session.add(Groups(name=request.form.get("name"), owner_id=current_user.id))
        db.session.commit()

        group = Groups.query.filter_by(name=request.form.get("name")).first()
        db.session.add(Members(group_id=group.id, user_id=current_user.id, is_owner=True))
        db.session.commit()

        flash("Successfully created Group!", "is-success")
        return redirect(url_for('groups.index'))

    flash("Couldn't create group. Please check the inputs!", "is-warning")
    return render_template("groups/create.html", form=group_form)


@groups.route("/<int:group_id>/delete")
@login_required
def delete(group_id):
    found_group = Groups.query.get(group_id)
    if found_group:
        db.session.delete(found_group)
        db.session.commit()

        flash(f"Group <{group_id}> successfully deleted!", "is-success")
        return redirect(url_for('groups.index'))

    flash(f"Couldn't find group <{group_id}>!", "is-warning")
    return redirect(url_for('groups.index'))




@groups.route("/<int:group_id>/profile")
def profile(group_id):
    found_group = Groups.query.get(group_id)
    if not found_group:
        flash("Could not find Group!", "is-warning")
        redirect(url_for('groups.index'))

    users = []
    for member in Members.query.filter_by(group_id=group_id).all():
        users.append((Users.query.get(member.user_id), member.is_owner))

    return render_template("groups/profile.html", group=found_group, users=users)


@groups.route("/<int:group_id>/join")
@login_required
def join(group_id):
    found_group = Groups.query.get(group_id)
    if not found_group:
        flash("Could not find group!", "is-warning")
        return redirect(url_for('groups.index'))

    if Members.query.filter_by(group_id=group_id, user_id=current_user.id).first():
        flash("You are already a member of this group!", "is-warning")
        return redirect(url_for('groups.profile', group_id=group_id))

    db.session.add(Members(group_id=found_group.id, user_id=current_user.id, is_owner=False))
    db.session.commit()

    flash("Successfully joined group!", "is-success")
    return redirect(url_for('groups.profile', group_id=group_id))


@groups.route("/<int:group_id>/leave")
@login_required
def leave(group_id):
    return "Sorry, the page was not implemneted yet!"


@groups.route("/<int:group_id>/kick/<int:user_id>")
@login_required
def kick(group_id, user_id):
    return "Sorry, the page was not implemneted yet!"


@groups.route("/<int:group_id>/draw_init")
@login_required
def raffle(group_id):
    return "Sorry, the page was not implemneted yet!"


@groups.route("/<int:group_id>/draw")
@login_required
def draw_name(group_id):
    return "Sorry, the page was not implemneted yet!"
