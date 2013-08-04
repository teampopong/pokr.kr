#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import Flask

from settings import API_SCRIPT_NAME, API_SERVER_SETTINGS


app = Flask(__name__)
app.debug = API_SERVER_SETTINGS['debug']


if not hasattr(app, '__loaded__'):
    from database import init_db
    from api import init_app
    from utils.reverse_proxy import init_app as init_reverse_proxy

    init_db(app)
    init_app(app)
    init_reverse_proxy(app, API_SCRIPT_NAME)

    setattr(app, '__loaded__', True)


if __name__ == '__main__':
    app.run(**API_SERVER_SETTINGS)

