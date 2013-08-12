# -*- coding: utf-8 -*-

from flask import request
from flask.ext.cache import Cache

from settings import CACHE_SETTINGS


cache = Cache()
CACHE_DEFAULT_TIMEOUT = 24 * 60 * 60


def init_cache(app):
    cache.init_app(app, config=CACHE_SETTINGS)
    with app.app_context():
        cache.clear()


def view_cache(timeout=CACHE_DEFAULT_TIMEOUT):
    return cache.cached(timeout, key_prefix=lambda: request.url)
