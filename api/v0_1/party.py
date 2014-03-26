# -*- coding: utf-8 -*-

from api.view import ApiView
from pokr.models.party import Party


class PartyApi(ApiView):
    model = Party

