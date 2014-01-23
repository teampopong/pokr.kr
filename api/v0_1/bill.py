# -*- coding: utf-8 -*-

from api.view import ApiView
from models.bill import Bill


class BillApi(ApiView):
    model = Bill

