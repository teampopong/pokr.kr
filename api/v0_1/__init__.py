# -*- coding: utf-8 -*-

def init_app(app):
    from api.v0_1.bill import init_app; init_app(app)
    from api.v0_1.party import init_app; init_app(app)
    from api.v0_1.person import init_app; init_app(app)
