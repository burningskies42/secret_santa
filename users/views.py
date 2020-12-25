from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from loguru import logger
from werkzeug.security import check_password_hash, generate_password_hash

from secret_santa import db
from secret_santa.models import Address, User
from secret_santa.users.forms import DeleteForm, UserEditForm, UserForm

users = Blueprint("users", __name__, template_folder="templates")


# Routes for handling user specific pages
@users.route("/")
@login_required
def profile():
    return render_template("users/index.html", title=f"Hello {current_user.name}!")


@users.route("/new")
def signup():
    user_form = UserForm()
    return render_template("users/signup.html", form=user_form)


@users.route("/new", methods=["POST"])
def signup_post():
    email = str.lower(request.form.get("email"))
    user = User.query.filter_by(email=email).first(email)
    if user:
        flash("Email address already exists", "is-warning")
        return redirect(url_for("users.signup"))

    user_form = UserForm(request.form)
    if user_form.validate():
        new_address = Address(description=request.form.get("address"))

        new_user = User(
            name=request.form.get("name"),
            email=str.lower(request.form.get("email")),
            password=generate_password_hash(request.form.get("password"), method="sha256"),
            address=new_address,
        )

        # add the new user to the database
        db.session.add(new_user)
        db.session.add(new_address)
        db.session.commit()

        flash("Successfully created user. Please log in!", "is-success")
        return redirect(url_for("auth.login"))
    else:
        flash("Couldn't create user. Please check the inputs!", "is-warning")
        return render_template("users/signup.html", form=user_form)


@users.route("/edit")
@login_required
def edit():
    logger.warning(f"id: {current_user.id}")
    found_user = User.query.get(current_user.id)
    # prefill edit form
    form = UserEditForm(obj=found_user)
    return render_template("users/user_edit.html", user=found_user, form=form)


@users.route("/edit", methods=["POST"])
@login_required
def edit_patch():
    user = User.query.get(current_user.id)
    # TODO: create EditForm() and adapt it here
    form = UserEditForm(request.form)
    # from IPython import embed; embed()
    if form.validate():
        # normal edit logic
        user.name = form.data["name"]
        user.email = str.lower(form.data["email"])

        address = Address().query.filter_by(user_id=user.id).first()
        address.description = form.data["address"]
        user.address = address
        db.session.add(user)
        db.session.add(address)
        db.session.commit()
        flash("Edited Successfully!", "is-success")
        return redirect(url_for("users.profile"))
    else:
        # if we fail to edit, show the edit page again with error messages and values that the user has typed in!
        flash("Could not edit user!", "is-danger")
        return render_template("users/user_edit.html", user=user, address=user.address, form=form)


@users.route("/delete", methods=["DELETE"])
@login_required
def delete():
    found_user = User.query.get(current_user.id)
    delete_form = DeleteForm(request.form)
    if delete_form.validate():
        # now that CSRF has been validated, user can be deleted
        db.session.delete(found_user)
        db.session.commit()
        flash("User Deleted!", "is-success")

        return render_template("home.html")
