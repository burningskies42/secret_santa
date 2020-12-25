import os

from flask import Flask, flash, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from loguru import logger

# init SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY") or os.urandom(24)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///santa.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    if os.environ.get("RESET_DB") == "1":
        with app.app_context():
            from secret_santa.models import Address, Group, Member, User

            db.create_all()
            db.session.commit()

    # register blueprints
    from secret_santa.templates.views import main as main_blueprint

    app.register_blueprint(main_blueprint)
    from secret_santa.auth.views import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    from secret_santa.users.views import users as users_blueprint

    app.register_blueprint(users_blueprint, url_prefix="/users")
    from secret_santa.groups.views import groups as groups_blueprint

    app.register_blueprint(groups_blueprint, url_prefix="/groups")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from secret_santa.models import User

        return User.query.get(int(user_id))

    limiter = Limiter(app, key_func=get_remote_address, default_limits=["5/second"])
    limiter.limit("60/hour")(auth_blueprint)

    # Redirect all non existent URLsto index.html
    @app.errorhandler(404)
    def page_not_found(e):
        flash("Ooops! The requested page doesn't exist!", "is-danger")

        return redirect(url_for("main.index"))

    return app
