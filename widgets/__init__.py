# -*- encoding: utf-8 -*-

from relation import relation
from timeline import timeline


__all__ = ['init_app']


widgets = {
    'relation': relation,
    'timeline': timeline,
}


def init_app(app):

    @app.context_processor
    def inject_widgets():
        return dict(widgets=widgets)
