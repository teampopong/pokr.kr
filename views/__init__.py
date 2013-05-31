# -*- encoding: utf-8 -*-

from flask.ext.babel import gettext


def init_app(app):
    gettext('home') # for babel extraction
    app.views = getattr(app, 'views', dict(home='main'))
    from views.bill import register; register(app)
    from views.main import register; register(app)
    from views.party import register; register(app)
    from views.person import register; register(app)
    from views.region import register; register(app)
    from views.search import register; register(app)
