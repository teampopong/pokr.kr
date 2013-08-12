# -*- coding: utf-8 -*-

from flask.ext.cache import Cache

from settings import CACHE_SETTINGS


cache = Cache()


def init_cache(app):
    cache.init_app(app, config=CACHE_SETTINGS)
    with app.app_context():
        cache.clear()
