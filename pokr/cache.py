# -*- coding: utf-8 -*-
# TODO: remove this

from flask_caching import Cache

from settings import CACHE_CONFIG


cache = Cache()


def init_cache(app):
    cache.init_app(app, config=CACHE_CONFIG)

