from flask import _app_ctx_stack, current_app
from pymongo import Connection
import memcache


def get_db():
    ctx = _app_ctx_stack.top
    cfg = current_app.config['DB_SETTINGS']
    con = getattr(ctx, 'db', None)
    if con is None:
        con = Connection(host=cfg['host'], port=cfg['port'])
        ctx.con = con
    return con[cfg['database']]


def get_cache():
    ctx = _app_ctx_stack.top
    cfg = current_app.config['CACHE_SETTINGS']
    cache = getattr(ctx, 'cache', None)
    if cache is None:
        cache = memcache.Client(['%s:%d' % (cfg['host'], cfg['port'])])
        ctx.cache = cache
    return cache

