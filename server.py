#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import Flask
from flask.ext.script import Manager

from settings import BABEL_SETTINGS, SCRIPT_NAME, SERVER_SETTINGS


app = Flask(__name__)
app.debug = SERVER_SETTINGS['debug']
manager = Manager(app, with_default_commands=False)


def init_modules():
    from flask.ext.assets import Environment as Asset
    from database import init_db
    from utils.assets import init_app as init_asset
    from utils.jinja import init_app as init_jinja
    from utils.i18n import PopongBabel
    from utils.linkall import init_app as init_linkall
    from utils.mobile import PopongMobile
    from utils.reverse_proxy import init_app as init_reverse_proxy
    from views import init_app as init_view
    from widgets import init_app as init_widgets

    Asset(app)
    init_asset(app)
    init_db(app)
    init_jinja(app)
    PopongBabel(app, **BABEL_SETTINGS)
    PopongMobile(app)
    init_linkall(app)
    init_reverse_proxy(app, SCRIPT_NAME)
    init_view(app)
    init_widgets(app)


@manager.command
def run():
    init_modules()
    app.run(**SERVER_SETTINGS)


# standalone mode
if __name__ == '__main__':
    manager.run()

# w/ WSGI
else:
    init_modules()
