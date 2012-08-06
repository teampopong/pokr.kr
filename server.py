#!/usr/bin/env python

from flask import _app_ctx_stack, Flask, jsonify, g
from flask.ext.assets import Environment as AssetEnvironment
from flask.ext.babel import Babel
import settings
from utils import mongojson_filter, LocaleError
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException


##### utils #####
class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = settings.SCRIPT_NAME
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


def create_server(name, **kwargs):
    '''Create Flask server with database and cache server connection.'''

    server = Flask(name, **kwargs)
    server.wsgi_app = ReverseProxied(server.wsgi_app)
    assets = AssetEnvironment(server)
    return server


def init_cache(server):
    server.config['CACHE_SETTINGS'] = settings.CACHE_SETTINGS

    @server.teardown_appcontext
    def close_cache(error=None):
        con = getattr(_app_ctx_stack.top, 'cache', None)
        if con is not None:
            con.disconnect_all()


def init_db(server):
    server.config['DB_SETTINGS'] = settings.DB_SETTINGS

    @server.teardown_appcontext
    def close_db(error=None):
        con = getattr(_app_ctx_stack.top, 'db', None)
        if con is not None:
            con.close()


def init_i18n(server):
    babel = Babel(server, **settings.BABEL_SETTINGS)

    @babel.localeselector
    def get_lang():
        locale = getattr(g, 'lang', None)
        if locale not in settings.LOCALES:
            # TODO: needs a page that handles exceptions
            raise LocaleError()
        return locale


def init_routes(server):
    '''
    Register all app modules specified in settings.
    '''

    default_locale = settings.BABEL_SETTINGS['default_locale']

    for url_prefix, app in settings.apps.items():

        @app.url_defaults
        def add_language_code(endpoint, values):
            values.setdefault('lang', getattr(g, 'lang', default_locale))

        @app.url_value_preprocessor
        def pull_lang_code(endpoint, values):
            g.lang = values.pop('lang', default_locale)

        server.register_blueprint(app, url_prefix=url_prefix)


def ensure_error_in_json(server):
    '''
    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    '''

    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    for code in default_exceptions.iterkeys():
        server.error_handler_spec[None][code] = make_json_error


def register_filters(server):
    server.jinja_env.filters['mongojson'] = mongojson_filter


def main():
    server = create_server(__name__)

    init_cache(server)
    init_db(server)
    init_i18n(server)
    init_routes(server)
    # ensure_error_in_json(server)
    register_filters(server)

    server.run(**settings.SERVER_SETTINGS)


##### main #####

if __name__ == '__main__':
    main()
