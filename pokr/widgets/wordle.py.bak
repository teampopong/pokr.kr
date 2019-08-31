# -*- coding: utf-8 -*-

from flask import render_template

from utils.jinja import guid_factory


def wordle(wordcounts, width, height, title=None, **kwargs):
    if wordcounts:
        max_count = float(max(wordcounts.itervalues()))
        wordweights = {
            key: value / max_count
            for key, value in wordcounts.iteritems()
        }
    else:
        wordweights = {}

    return render_template('widgets/wordle.html', wordweights=wordweights,
            width=width, height=height, guids=guid_factory(), title=title, **kwargs)

