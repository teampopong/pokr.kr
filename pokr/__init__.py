# -*- coding: utf-8 -*-

from flask import Flask


app = Flask(__name__)
app.config.from_object('settings')


@app.before_first_request
def init():
    from flask.ext.assets import Environment as Asset

    from pokr.cache import init_cache
    from pokr.controllers import init_controller
    from pokr.database import init_db
    from utils.assets import init_app as init_asset
    from utils.jinja import init_app as init_jinja
    from utils.i18n import PopongBabel
    from utils.linkall import init_app as init_linkall
    from utils.login import init_app as init_login
    from utils.mobile import PopongMobile
    from utils.reverse_proxy import init_app as init_reverse_proxy
    from pokr.views import init_app as init_view
    from pokr.widgets import init_app as init_widgets

    Asset(app)
    init_cache(app)
    init_controller(app)
    init_asset(app)
    init_db(app)
    init_jinja(app)
    PopongBabel(app)
    PopongMobile(app)
    init_linkall(app)
    init_login(app)
    init_reverse_proxy(app)
    init_view(app)
    init_widgets(app)

    setattr(app, '__loaded__', True)

