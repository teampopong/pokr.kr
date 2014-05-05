# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.assets import Environment as Asset

from pokr.cache import init_cache
from pokr.database import Database
from pokr.login import Login
from pokr.models import patch_all; patch_all()
from pokr.views import init_app as init_view
from pokr.widgets import init_app as init_widgets
from utils.assets import init_app as init_asset
from utils.jinja import init_app as init_jinja
from utils.i18n import PopongBabel
from utils.linkall import init_app as init_linkall
from utils.mobile import PopongMobile
from utils.reverse_proxy import init_app as init_reverse_proxy


app = Flask(__name__)
app.config.from_object('settings')


Asset(app)
init_cache(app)
init_asset(app)
Database(app)
init_jinja(app)
PopongBabel(app)
PopongMobile(app)
init_linkall(app)
Login(app)
init_reverse_proxy(app)
init_view(app)
init_widgets(app)

