# -*- coding: utf-8 -*-

from flask import request

from api import ApiModelView, ApiSearchView
from models.person import Person


class PersonApi(ApiModelView):
    model = Person


class PersonSearchApi(ApiSearchView):
    model = Person


def init_app(app):
    person_view = PersonApi.as_view('person_api')
    search_view = PersonSearchApi.as_view('person_search_api')
    app.add_url_rule('/v0.1/person/', defaults={'id': None},
                     view_func=person_view, methods=['GET'])
    app.add_url_rule('/v0.1/person/search',
                     view_func=search_view, methods=['GET'])
    app.add_url_rule('/v0.1/person/<int:id>', view_func=person_view,
                     methods=['GET'])
