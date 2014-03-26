# -*- coding: utf-8 -*-

from api.view import ApiView
from pokr.models.bill import Bill


class BillApi(ApiView):
    model = Bill

