#!/usr/bin/env python

from bson.objectid import ObjectId
from flask import _app_ctx_stack, current_app, Response
from functools import wraps
import json
from json import JSONEncoder
import memcache
from pymongo import Connection
from pymongo.cursor import Cursor

class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, Cursor):
            return list(obj)
        else:
            return JSONEncoder.default(self, obj, **kwargs)


class LocaleError(Exception):
    pass

def response_json(f):

    @wraps(f)
    def interface(*args, **kwargs):
        obj = f(*args, **kwargs)
        text = json.dumps(obj, indent=2, encoding='utf-8', cls=MongoEncoder)
        return Response(text, mimetype='application/json')

    return interface

def mongojson_filter(s):
    return json.dumps(s, indent=2, encoding='utf-8', cls=MongoEncoder)

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
