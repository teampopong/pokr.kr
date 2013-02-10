# -*- encoding: utf-8 -*-

def register_all(app):
    from views.main import register; register(app)
    from views.party import register; register(app)
    from views.person import register; register(app)
