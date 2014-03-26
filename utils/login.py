# -*- codiing: utf-8 -*-
# TODO: should be inside pokr app

from pokr.database import Base, db_session


def init_app(app):
    from flask.ext import login
    login_manager = login.LoginManager()
    login_manager.login_view = 'login'
    login_manager.login_message = ''
    login_manager.setup_app(app)

    from social.apps.flask_app.routes import social_auth
    app.register_blueprint(social_auth)

    from pokr.models.user import User
    @login_manager.user_loader
    def load_user(userid):
        try:
            return User.query.get(int(userid))
        except (TypeError, ValueError):
            pass


def init_db(app):
    from social.apps.flask_app import models
    from social.apps.flask_app.models import init_social
    social_storage = init_social(app, Base, db_session)

