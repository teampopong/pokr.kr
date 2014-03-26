# -*- encoding: utf-8 -*-

from .card import card
from .histogram import histogram
from .kmap import kmap
from .relation import rivals
from .timeline import timeline
from .wordle import wordle


__all__ = ['init_app']


widgets = {
    'card': card,
    'histogram': histogram,
    'kmap': kmap,
    'rivals': rivals,
    'timeline': timeline,
    'wordle': wordle,
}


def init_app(app):

    @app.context_processor
    def inject_widgets():
        return dict(widgets=widgets)
