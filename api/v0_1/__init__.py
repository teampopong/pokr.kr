# -*- coding: utf-8 -*-

def init_app(app):
    from api.v0_1.person import init_app as init_person
    init_person(app)
