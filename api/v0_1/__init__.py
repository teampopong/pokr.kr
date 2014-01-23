# -*- coding: utf-8 -*-

def init_app(app):
    from api import register_api
    from api.v0_1.bill import BillApi
    from api.v0_1.party import PartyApi
    from api.v0_1.person import PersonApi

    register_api(app, BillApi, 'bill_api', '/v0.1/bill/', pk_type='string')
    register_api(app, PartyApi, 'party_api', '/v0.1/party/')
    register_api(app, PersonApi, 'person_api', '/v0.1/person/')

