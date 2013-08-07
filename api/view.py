# -*- coding: utf-8 -*-

from flask import abort, request
from flask.ext.sqlalchemy import BaseQuery
from flask.views import MethodView

from utils.jsonify import jsonify


class ApiView(MethodView):
    model = None

    def get(self, _type=None, **kwargs):
        if _type == 'single':
            return self.get_single(**kwargs)
        elif _type == 'search':
            return self.search(**kwargs)
        elif _type == 'list':
            return self.get_list(**kwargs)
        raise Exception('unknown api request type: %s' % _type)

    def get_single(self, id, **kwargs):
        query = self._query.filter_by(id=id)
        return self._jsonify_single(query)

    def get_list(self, **kwargs):
        return self._jsonify_list(self._query)

    def search(self, **kwargs):
        return self._jsonify_list(self._search())

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
        entity = query.first()
        if not entity:
            abort(404)

        result = self._to_dict(entity)
        result['kind'] = self.model.kind('single')
        return jsonify(result)

    def _jsonify_list(self, query):
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

