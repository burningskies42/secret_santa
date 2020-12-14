import os
from loguru import logger

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
# from flask_ipban import IpBan

from .auth import auth as auth_blueprint
from .secretsanta import main as main_blueprint
from .utils import reset_database


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    if os.environ.get("RESET_DB") == "1":
        reset_database()

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return "TRUE'ish"

    #TODO: check if grinch-safe
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["1/second"]
    )
    limiter.limit("60/hour")(auth_blueprint)

    return app
