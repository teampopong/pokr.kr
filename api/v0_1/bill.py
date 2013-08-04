# -*- coding: utf-8 -*-

from flask import abort

from api import ApiModelView, ApiSearchView
from models.bill import Bill


class BillApi(ApiModelView):
    model = Bill


class BillSearchApi(ApiSearchView):
    model = Bill


def init_app(app):
    bill_view = BillApi.as_view('bill_api')
    search_view = BillSearchApi.as_view('bill_search_api')
    app.add_url_rule('/v0.1/bill/', defaults={'id': None},
                     view_func=bill_view, methods=['GET'])
    app.add_url_rule('/v0.1/bill/search',
                     view_func=search_view, methods=['GET'])
    app.add_url_rule('/v0.1/bill/<id>', view_func=bill_view,
                     methods=['GET'])
