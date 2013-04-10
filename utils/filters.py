# -*- encoding: utf-8 -*-

import json
from sqlalchemy.ext.declarative import DeclarativeMeta
import uuid


def init_app(app):
    app.jinja_env.filters['jsonify'] = jsonify


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj, **kwargs):
        # handles SQLAlchemy object
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj, **kwargs)

def jsonify(s):
    return json.dumps(s, indent=2, encoding='utf-8', cls=MyJSONEncoder)

def guid_factory():
    guids = {}

    def factory(key):
        val = guids.get(key)
        if not val:
            val = 'u%s' % uuid.uuid4().hex[:8]
            guids[key] = val
        return val

    return factory
