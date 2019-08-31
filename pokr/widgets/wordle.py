# -*- coding: utf-8 -*-

from __future__ import division
from past.utils import old_div
from flask import render_template

from utils.jinja import guid_factory


def wordle(wordcounts, width, height, title=None, **kwargs):
    if wordcounts:
        max_count = float(max(wordcounts.values()))
        wordweights = {
            key: old_div(value, max_count)
            for key, value in wordcounts.items()
        }
    else:
        wordweights = {}

    return render_template('widgets/wordle.html', wordweights=wordweights,
            width=width, height=height, guids=guid_factory(), title=title, **kwargs)

