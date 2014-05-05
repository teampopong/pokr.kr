# -*- codiing: utf-8 -*-


class Login(object):
    def __init__(self, app):
        self.app = app

        from flask.ext.login import LoginManager
        login_manager = LoginManager()
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

