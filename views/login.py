#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import g, render_template, redirect, request, url_for
from flask.ext.login import current_user, login_required, logout_user

from social.apps.flask_app.template_filters import backends


def register(app):

    @login_required
    @app.route('/done/')
    def done():
        return redirect(request.referrer or url_for('main'))

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(request.referrer or url_for('main'))

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

