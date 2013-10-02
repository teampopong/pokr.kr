#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import g, render_template, redirect
from flask.ext.login import current_user, login_required, logout_user

from social.apps.flask_app.template_filters import backends


def register(app):

    @app.route('/login')
    def login():
        return render_template('login.html')

    @login_required
    @app.route('/done/')
    def done():
        return render_template('login-done.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect('/')

    @app.before_request
    def global_user():
        g.user = current_user

    @app.context_processor
    def inject_user():
        user = getattr(g, 'user')
        return {
            'user': user,
            'is_logged': user and not user.is_anonymous()
        }

    app.context_processor(backends)

