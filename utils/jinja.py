# -*- encoding: utf-8 -*-

import uuid

from flask import request, url_for
from flask.ext.babel import gettext
from werkzeug.urls import Href, url_unquote

from .jsonify import jsonify
from pokr.models.assembly import term as assembly_term # FIXME: no dep. w/ pokr
from pokr.models.election import current_parliament_id


breadcrumb_home = ['home']


def init_app(app):
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.jinja_env.filters['jsonify'] = jsonify
    app.jinja_env.globals.update(
        hasattr=hasattr,
        int=int,
        max=max,
        min=min,
        zip=zip,
    )
    app.jinja_env.globals.update(
        app=app,
        assembly_term=assembly_term,
        current_parliament_id=current_parliament_id,
        url_for_query=url_for_query,
        url_for_noencode=url_for_noencode,
    )

    app.breadcrumbed_views = {}
    @app.context_processor
    def inject_breadcrumb():
        if request.endpoint not in app.breadcrumbed_views:
            return {}

        breadcrumbs = app.breadcrumbed_views.get(request.endpoint, [])
        return dict(breadcrumbs=breadcrumbs)


def guid_factory():
    guids = {}

    def factory(key):
        val = guids.get(key)
        if not val:
            val = 'u%s' % uuid.uuid4().hex[:8]
            guids[key] = val
        return val

    return factory


def url_for_query(**kwargs):
    h = Href(request.base_url)
    args = dict(request.args, **kwargs)
    return h(**args)


def url_for_noencode(endpoint, **kwargs):
    return url_unquote(url_for(endpoint, **kwargs))


def breadcrumb(app, *hierarchy):
    def decorator(f):
        app.breadcrumbed_views[f.__name__] = breadcrumb_home + list(hierarchy)
        return f
    return decorator
