# -*- coding: utf-8 -*-
# TODO: remove this

from flask.ext.cache import Cache

from conf.storage import CACHE_CONFIG


cache = Cache()


def init_cache(app):
    cache.init_app(app, config=CACHE_CONFIG)

