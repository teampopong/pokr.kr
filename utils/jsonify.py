# -*- coding: utf-8 -*-

from datetime import date
import json

from sqlalchemy.ext.declarative import DeclarativeMeta


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

        elif isinstance(obj, date):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj, **kwargs)


def jsonify(s):
    return json.dumps(s, indent=2, encoding='utf-8', cls=MyJSONEncoder)

