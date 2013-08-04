# -*- coding: utf-8 -*-

from flask import abort

from api.utils import ApiModelView
from models.person import Person


class PersonAPI(ApiModelView):
    model = Person


def init_view(app):
    person_view = PersonAPI.as_view('person_api')
    app.add_url_rule('/person/', defaults={'id': None},
                     view_func=person_view, methods=['GET'])
    app.add_url_rule('/person/<int:id>', view_func=person_view,
                     methods=['GET'])
