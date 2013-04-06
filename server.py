#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import _app_ctx_stack, Flask, request, url_for
from flask.ext.babel import Babel

from database import init_db
import settings
from utils.assets import asset
from utils.host import host
from utils.i18n import get_locale, name2eng, party2eng
from utils.filters import jsonify
from utils.linkall import LinkAllFilter
from widgets import widgets


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




app = Flask(__name__)
app.debug = settings.SERVER_SETTINGS['debug']
app.wsgi_app = ReverseProxied(app.wsgi_app)


def init_i18n():
    babel = Babel(app, **settings.BABEL_SETTINGS)
    babel.localeselector(get_locale)


def init_routes():
    '''
    Register all app modules specified in settings.
    '''

    from views import register_all; register_all(app)


def register_filters():
    app.jinja_env.filters['jsonify'] = jsonify
    app.jinja_env.filters['name2eng'] = name2eng
    app.jinja_env.filters['party2eng'] = party2eng

    # FIXME: keyword source
    with open('keywords.txt', 'r') as f:
        keywords = f.read().decode('utf-8').split()
    url_map = lambda keyword: url_for('entity_page', keyword=keyword)
    any_re = '|'.join(keywords + ['[1-9][0-9]{3}'])
    linkall = LinkAllFilter(url_map, any_re).get()
    app.jinja_env.filters['linkall'] = linkall


def register_context_processors():

    @app.context_processor
    def inject_asset():
        return dict(asset=asset)

    @app.context_processor
    def inject_widgets():
        return dict(widgets=widgets)

    @app.context_processor
    def inject_locales():
        locale_links = dict((locale, request.url.replace(request.host, host(locale)))
                for locale in settings.LOCALES)
        return dict(locale_links=locale_links,
                locale=get_locale())


##### setup #####

init_db()
init_i18n()
init_routes()

register_filters()
register_context_processors()


##### main #####

if __name__ == '__main__':
    app.run(**settings.SERVER_SETTINGS)
