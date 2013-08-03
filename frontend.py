#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse

from flask import Flask

from settings import BABEL_SETTINGS, SCRIPT_NAME, SERVER_SETTINGS


app = Flask(__name__)
app.debug = SERVER_SETTINGS['debug']


if not hasattr(app, '__loaded__'):
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

    setattr(app, '__loaded__', True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', dest='locale', default='auto',
                        help='force locale (e.g. en, kr)')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.locale in app.LOCALES:
        app.babel.force_locale(args.locale)
    app.run(**SERVER_SETTINGS)

