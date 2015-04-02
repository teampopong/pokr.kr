# -*- encoding: utf-8 -*-

from .bubble import bubble
from .card import card
from .histogram import histogram
from .kmap import kmap
from .relation import rivals
from .timeline import timeline
from .wordle import wordle
from .year import year


__all__ = ['init_app']


widgets = {
    'bubble': bubble,
    'card': card,
    'histogram': histogram,
    'kmap': kmap,
    'rivals': rivals,
    'timeline': timeline,
    'wordle': wordle,
    'year': year,
}


def init_app(app):

    @app.context_processor
    def inject_widgets():
        return dict(widgets=widgets)
