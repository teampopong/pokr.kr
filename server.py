#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import Flask

from database import init_db
from utils.assets import init_app as init_asset
from utils.filters import init_app as init_filters
from utils.i18n import init_app as init_i18n
from utils.linkall import init_app as init_linkall
from utils.reverse_proxy import init_app as init_reverse_proxy
from views import init_app as init_view
from widgets import init_app as init_widgets
import settings




app = Flask(__name__)
app.debug = settings.SERVER_SETTINGS['debug']


init_asset(app)
init_db()
init_filters(app)
init_i18n(app, **settings.BABEL_SETTINGS)
init_linkall(app)
init_reverse_proxy(app, settings.SCRIPT_NAME)
init_view(app)
init_widgets(app)


if __name__ == '__main__':
    app.run(**settings.SERVER_SETTINGS)
