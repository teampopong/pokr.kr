# -*- coding: utf-8 -*-

from api.view import ApiView
from models.person import Person


class PersonApi(ApiView):
    model = Person

