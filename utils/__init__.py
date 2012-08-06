#!/usr/bin/env python

from bson.objectid import ObjectId
import flask
from flask import g, Response
from functools import wraps
import json
from json import JSONEncoder
from pymongo.cursor import Cursor

class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, Cursor):
            return list(obj)
        else:
            return JSONEncoder.default(self, obj, **kwargs)

def response_json(f):

    @wraps(f)
    def interface(*args, **kwargs):
        obj = f(*args, **kwargs)
        text = json.dumps(obj, indent=2, encoding='utf-8', cls=MongoEncoder)
        return Response(text, mimetype='application/json')

    return interface

def patch_url_for():
    original_url_for = flask.url_for
    def url_for_with_lang(endpoint, **values):
        if endpoint != 'static' and 'lang' not in values:
            values['lang'] = g.lang if hasattr(g, 'lang') else None
        return original_url_for(endpoint, **values)
    flask.url_for = url_for_with_lang

def patch_template_url_for(app):

    @app.context_processor
    def replace_url_for():
        return dict(url_for=flask.url_for)

def mongojson_filter(s):
    return json.dumps(s, indent=2, encoding='utf-8', cls=MongoEncoder)

