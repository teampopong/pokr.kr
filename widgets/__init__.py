# -*- encoding: utf-8 -*-

from card import card
from relation import relation
from timeline import timeline


__all__ = ['init_app']


widgets = {
    'card': card,
    'relation': relation,
    'timeline': timeline,
}


def init_app(app):

    @app.context_processor
    def inject_widgets():
        return dict(widgets=widgets)
