# -*- encoding: utf-8 -*-

from card import card
from kmap import kmap
from relation import rivals
from timeline import timeline


__all__ = ['init_app']


widgets = {
    'card': card,
    'kmap': kmap,
    'rivals': rivals,
    'timeline': timeline,
}


def init_app(app):

    @app.context_processor
    def inject_widgets():
        return dict(widgets=widgets)
