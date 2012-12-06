#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import _app_ctx_stack, Flask, g
from flask.ext.assets import Environment as AssetEnvironment
from flask.ext.babel import Babel
import settings
from utils.mongodb import mongojsonify
from utils.i18n import LocaleError, name2eng, party2eng
from utils.linkall import LinkAllFilter


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
            raise LocaleError(locale)
        return locale


def init_routes(server):
    '''
    Register all app modules specified in settings.
    '''

    @server.route('/entity/<keyword>')
    def entity_page(keyword):
        return keyword + u'의 페이지입니다'

    default_locale = settings.BABEL_SETTINGS['default_locale']

    for url_prefix, app in settings.apps.items():

        @app.url_defaults
        def add_language_code(endpoint, values):
            values.setdefault('lang', getattr(g, 'lang', default_locale))

        @app.url_value_preprocessor
        def pull_lang_code(endpoint, values):
            g.lang = values.pop('lang', default_locale)

        server.register_blueprint(app, url_prefix=url_prefix)


def register_filters(server):
    server.jinja_env.filters['mongojsonify'] = mongojsonify
    server.jinja_env.filters['name2eng'] = name2eng
    server.jinja_env.filters['party2eng'] = party2eng

    # FIXME: keyword source
    with open('keywords.txt', 'r') as f:
        keywords = f.read().decode('utf-8').split()
    url_map = lambda keyword: '/entity/%s' % keyword
    any_re = '|'.join(keywords + ['[1-9][0-9]{3}'])
    linkall = LinkAllFilter(url_map, any_re).get()
    server.jinja_env.filters['linkall'] = linkall


def main():
    server = create_server(__name__)

    init_cache(server)
    init_db(server)
    init_i18n(server)
    init_routes(server)

    register_filters(server)

    server.run(**settings.SERVER_SETTINGS)


##### main #####

if __name__ == '__main__':
    main()
