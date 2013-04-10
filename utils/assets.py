#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import current_app, url_for, request


def init_app(app):
    @app.context_processor
    def inject_asset():
        return dict(asset=asset)


def asset(relpath):
    if current_app.debug:
        return url_for('static', filename=relpath)
    else:
        return '//{host}/static/{path}'.format(host=request.host, path=relpath)
