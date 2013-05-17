# -*- encoding: utf-8 -*-

import json
import uuid

from flask import request, url_for
from flask.ext.babel import gettext
from sqlalchemy.ext.declarative import DeclarativeMeta
from werkzeug.urls import Href


breadcrumb_home = ['home']


def init_app(app):
    app.jinja_env.filters['jsonify'] = jsonify
    app.jinja_env.globals.update(zip=zip, max=max, int=int, app=app)
    app.jinja_env.globals.update(url_for_query=url_for_query)

    app.breadcrumbed_views = {}
    @app.context_processor
    def inject_breadcrumb():
        if request.endpoint not in app.breadcrumbed_views:
            return {}

        breadcrumbs = app.breadcrumbed_views.get(request.endpoint, [])
        return dict(breadcrumbs=breadcrumbs)


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj, **kwargs):
        # handles SQLAlchemy object
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj, **kwargs)


def jsonify(s):
    return json.dumps(s, indent=2, encoding='utf-8', cls=MyJSONEncoder)


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


def breadcrumb(app, *hierarchy):
    def decorator(f):
        app.breadcrumbed_views[f.__name__] = breadcrumb_home + list(hierarchy)
        return f
    return decorator
