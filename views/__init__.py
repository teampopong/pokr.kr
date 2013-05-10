# -*- encoding: utf-8 -*-

def init_app(app):
    from views.bill import register; register(app)
    from views.main import register; register(app)
    from views.party import register; register(app)
    from views.person import register; register(app)
    from views.region import register; register(app)
    from views.school import register; register(app)
