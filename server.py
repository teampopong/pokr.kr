#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import Flask

from database import init_db
from utils.assets import init_app as init_asset
from utils.filters import init_app as init_filters
from utils.i18n import PopongBabel
from utils.linkall import init_app as init_linkall
from utils.mobile import PopongMobile
from utils.reverse_proxy import init_app as init_reverse_proxy
from views import init_app as init_view
from widgets import init_app as init_widgets
from settings import BABEL_SETTINGS, SCRIPT_NAME, SERVER_SETTINGS




app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)
app.debug = SERVER_SETTINGS['debug']


init_asset(app)
init_db(app)
init_filters(app)
PopongBabel(app, **BABEL_SETTINGS)
PopongMobile(app)
init_linkall(app)
init_reverse_proxy(app, SCRIPT_NAME)
init_view(app)
init_widgets(app)


if __name__ == '__main__':
    app.run(**SERVER_SETTINGS)
