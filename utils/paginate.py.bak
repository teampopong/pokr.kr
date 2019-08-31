# -*- coding: utf-8 -*-

from flask import url_for


class MoreQuery(object):
    def __init__(self, Model, view, order, target='items', pagesize=10):
        if order not in ['asc', 'desc']:
            raise RuntimeError()

        self.Model = Model
        self.view = getattr(view, '__name__', view)
        self.order = order
        self.pagesize = pagesize
        self.target = target

    def query(self, q, _from=None, pagesize=None):
        if not q:
            return None

        pagesize = pagesize or self.pagesize
        data = {}

        if _from:
            if self.order == 'asc':
                q = q.filter(self.Model.id >= _from)
            else:
                q = q.filter(self.Model.id <= _from)

        items = q.limit(pagesize + 1).all()
        data[self.target] = items[:pagesize]

        if len(items) > pagesize:
            if self.order == 'asc':
                _next = url_for(self.view, after=items[-1].id)
            else:
                _next = url_for(self.view, before=items[-1].id)
            data['next'] = _next

        return data

