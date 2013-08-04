# -*- coding: utf-8 -*-

import json

from datetime import date
from flask import abort, request
from flask.views import MethodView
from flask.ext.sqlalchemy import BaseQuery
from sqlalchemy.ext.declarative import DeclarativeMeta


def init_app(app):
    from api.v0_1 import init_app; init_app(app)


class ApiView(MethodView):
    model = None

    @property
    def _query(self):
        if not self.model:
            raise NotImplementedError()

        return BaseQuery(self.model, self.model.query.session)

    def _to_dict(self, entity):
        return entity.to_dict(projection=request.args.get('projection'))

    def _jsonify_single(self, query):
        entity = query.first()
        if not entity:
            abort(404)

        result = self._to_dict(entity)
        result['kind'] = self.model.kind('single')
        return jsonify(result)

    def _jsonify_list(self, query):
        page = query.paginate(int(request.args.get('page', 1)),
                              int(request.args.get('maxResults', 20)))

        result = {}
        result['kind'] = self.model.kind('list')
        result['items'] = [self._to_dict(entity) for entity in page.items]
        if page.has_prev:
            result['prevPage'] = page.prev_num
        if page.has_next:
            result['nextPage'] = page.next_num

        return jsonify(result)


class ApiModelView(ApiView):
    def get(self, id):
        if id is None:
            return self.get_all()

        query = self._query.filter_by(id=id)
        return self._jsonify_single(query)

    def get_all(self):
        return self._jsonify_list(self._query)


class ApiSearchView(ApiView):
    def get(self):
        query = self.search()
        return self._jsonify_list(query)

    def search(self):
        if not self.model or not hasattr(self.model, 'name'):
            raise NotImplementedError()

        q = request.args.get('q', '')
        return self._query.filter(self.model.name.like(u'%{q}%'.format(q=q)))



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
        return self._to_dict_light()

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

        elif isinstance(obj, date):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj, **kwargs)


def jsonify(s):
    return json.dumps(s, indent=2, encoding='utf-8', cls=MyJSONEncoder)


