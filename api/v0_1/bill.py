# -*- coding: utf-8 -*-

from flask import abort

from api import ApiModelView
from models.bill import Bill


class BillApi(ApiModelView):
    model = Bill


def init_app(app):
    bill_view = BillApi.as_view('bill_api')
    app.add_url_rule('/v0.1/bill/', defaults={'id': None},
                     view_func=bill_view, methods=['GET'])
    app.add_url_rule('/v0.1/bill/<id>', view_func=bill_view,
                     methods=['GET'])
