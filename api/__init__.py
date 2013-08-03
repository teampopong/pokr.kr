# -*- coding: utf-8 -*-

import json

from flask import request
from flask.views import MethodView
from sqlalchemy.ext.declarative import DeclarativeMeta


class ApiModelView(MethodView):
    model = None

    def get(self, id):
        if not self.model:
            raise NotImplementedError()

        if id is None:
            return self.get_all()

        entity = self.model.query.filter_by(id=id).first()
        if not entity:
            abort(404)

        result = self._to_dict(entity)
        result['kind'] = self.model.kind('single')
        return jsonify(result)

    def get_all(self):
        result = {}
        result['kind'] = self.model.kind('list')
        # FIXME: pagenation
        result['items'] = [self._to_dict(entity) for entity in model.query]
        return jsonify(result)

    def _to_dict(self, entity):
        return entity.to_dict(projection=request.args.get('projection'))


class ApiModel(object):
    __kind_top__ = 'gov'
    __kind_single__ = None
    __kind_list__ = None

    def to_dict(self, projection=None):
        if not hasattr(self, '__table__'):
            raise Exception('ApiModel should inherit `Base` class')

        projection = projection or 'light'
        if projection == 'light':
            return self._to_dict_light()
        elif projection == 'full':
            return self._to_dict_full()
        else:
            raise Exception('Unknown argument')

    @classmethod
    def kind(cls, projection):
        if projection == 'single':
            return '%s#%s' % (cls.__kind_top__, cls.__kind_single__)
        elif projection == 'list':
            return '%s#%s' % (cls.__kind_top__, cls.__kind_list__)
        else:
            raise Exception('Unknown argument')

    def _to_dict_light(self):
        return self._columns_to_dict()

    def _to_dict_full(self):
        return self._columns_to_dict()

    def _columns_to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)

        return d


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


