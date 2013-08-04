# -*- coding: utf-8 -*-

from flask import abort

from api import ApiModelView, ApiSearchView
from models.party import Party


class PartyApi(ApiModelView):
    model = Party


class PartySearchApi(ApiSearchView):
    model = Party


def init_app(app):
    party_view = PartyApi.as_view('party_api')
    search_view = PartySearchApi.as_view('party_search_api')
    app.add_url_rule('/v0.1/party/', defaults={'id': None},
                     view_func=party_view, methods=['GET'])
    app.add_url_rule('/v0.1/party/search',
                     view_func=search_view, methods=['GET'])
    app.add_url_rule('/v0.1/party/<int:id>', view_func=party_view,
                     methods=['GET'])
