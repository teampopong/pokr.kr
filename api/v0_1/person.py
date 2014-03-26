# -*- coding: utf-8 -*-

from api.view import ApiView
from pokr.models.person import Person


class PersonApi(ApiView):
    model = Person

