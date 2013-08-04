# -*- coding: utf-8 -*-

from flask import abort

from api import ApiModelView
from models.party import Party


class PartyApi(ApiModelView):
    model = Party


def init_app(app):
    party_view = PartyApi.as_view('party_api')
    app.add_url_rule('/v0.1/party/', defaults={'id': None},
                     view_func=party_view, methods=['GET'])
    app.add_url_rule('/v0.1/party/<int:id>', view_func=party_view,
                     methods=['GET'])
