# -*- encoding: utf-8 -*-

from flask.ext.babel import gettext


def init_app(app):
    gettext('home') # for babel extraction
    app.views = getattr(app, 'views', dict(home='main'))
    from .bill import register; register(app)
    from .login import register; register(app)
    from .main import register; register(app)
    from .meeting import register; register(app)
    from .mypage import register; register(app)
    from .party import register; register(app)
    from .person import register; register(app)
    from .region import register; register(app)
    from .search import register; register(app)
    from .statement import register; register(app)
