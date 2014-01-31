# -*- coding: utf-8 -*-

from flask import abort, request
from flask.ext.sqlalchemy import BaseQuery
from flask.views import MethodView

from utils.jsonify import jsonify


class ApiView(MethodView):
    '''Create basic REST HTTP endpoints for a single resource type.
    To create the endpoints, an API view class may inherit this class.
    The view subclass should have :attr:`model` which inherits :class:`ApiModel`.

        class PersonApi(ApiView):
            model = Person
            ...

        class Person(ApiModel):
            ...
    '''
    model = None

    def get(self, _type=None, **kwargs):
        '''Dispatch GET request to an appropriate handler based on the `type`'''
        if _type == 'single':
            return self.get_single(**kwargs)
        elif _type == 'search':
            return self.get_list(self._search(), **kwargs)
        elif _type == 'list':
            return self.get_list(self._query, **kwargs)
        raise Exception('unknown api request type: %s' % _type)

    def get_single(self, id, **kwargs):
        '''Find a entry with `id` and return in JSON format.'''
        query = self._query.filter_by(id=id)
        return self._jsonify_single(query)

    def get_list(self, query, **kwargs):
        '''Return filtered/sorted entry list'''
        if request.args.get('sort'):
            key = request.args.get('sort')
            order = request.args.get('order', 'desc')
            query = self._sort(query, key, order)

        return self._jsonify_list(query)

    def _sort(self, query, key, order):
        if not hasattr(self.model, key):
            raise Exception('unknown sorting criteria: %s' % key)
        if order not in ['asc', 'desc']:
            raise Exception('unknown sorting order: %s' % order)

        key = getattr(self.model, key)
        if order == 'desc':
            key = key.desc()

        return query.order_by(key)

    def _search(self):
        if not self.model or not hasattr(self.model, 'name'):
            raise NotImplementedError()

        q = request.args.get('q', '')
        return self._query.filter(self.model.name.like(u'%{q}%'.format(q=q)))

    @property
    def _query(self):
        if not self.model:
            raise NotImplementedError()

        return BaseQuery(self.model, self.model.query.session)

    def _to_dict(self, entity):
        return entity.to_dict(projection=request.args.get('projection'))

    def _jsonify_single(self, query):
        '''Compose a `single`-typed response data.'''
        entity = query.first()
        if not entity:
            abort(404)

        result = self._to_dict(entity)
        result['kind'] = self.model.kind('single')
        return jsonify(result)

    def _jsonify_list(self, query):
        '''Compose a `list`/`search`-typed response data.'''
        page = query.paginate(int(request.args.get('page', 1)),
                              int(request.args.get('per_page', 20)))

        result = {}
        result['kind'] = self.model.kind('list')
        result['items'] = [self._to_dict(entity) for entity in page.items]
        if page.has_prev:
            result['prev_page'] = page.prev_num
        if page.has_next:
            result['next_page'] = page.next_num

        return jsonify(result)

