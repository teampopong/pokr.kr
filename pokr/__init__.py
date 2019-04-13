# -*- coding: utf-8 -*-

from flask import Flask


app = Flask(__name__)
app.config.from_object('settings')


def bootstrap():
    from flask_assets import Environment as Asset; Asset(app)

    from pokr.cache import init_cache; init_cache(app)
    from pokr.controllers import init_controller; init_controller(app)
    from pokr.database import init_db; init_db(app)
    from utils.assets import init_app as init_asset; init_asset(app)
    from utils.jinja import init_app as init_jinja; init_jinja(app)
    from utils.i18n import PopongBabel; PopongBabel(app)
    from utils.linkall import init_app as init_linkall; init_linkall(app)
    from utils.login import init_app as init_login; init_login(app)
    from utils.mobile import PopongMobile; PopongMobile(app)
    from utils.reverse_proxy import init_app as init_reverse_proxy; init_reverse_proxy(app)
    from pokr.views import init_app as init_view; init_view(app)
    from pokr.widgets import init_app as init_widgets; init_widgets(app)

