# -*- coding: utf-8 -*-

from api.view import ApiView
from models.party import Party


class PartyApi(ApiView):
    model = Party

