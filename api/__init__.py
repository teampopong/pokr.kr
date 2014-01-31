# -*- coding: utf-8 -*-

def init_app(app):
    from api.v0_1 import init_app; init_app(app)


def register_api(app, view, endpoint, url, pk_type='int'):
    '''Register an API resource::

        register_api(app, BillApi, 'bill_api', '/v0.1/bill/', pk_type='string')
    '''
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, view_func=view_func,
                     defaults={'_type': 'list'}, methods=['GET',])
    app.add_url_rule('%ssearch' % (url), view_func=view_func,
                     defaults={'_type': 'search'}, methods=['GET',])
    app.add_url_rule('%s<%s:id>' % (url, pk_type), view_func=view_func,
                     defaults={'_type': 'single'}, methods=['GET'])

