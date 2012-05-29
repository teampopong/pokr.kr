#!/usr/bin/env python

from bson.objectid import ObjectId
from flask import Response
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
