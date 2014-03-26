# -*- coding: utf-8 -*-

from flask import render_template

from utils.jinja import guid_factory


def histogram(value, values, **kwargs):
    values = map(str, values)
    return render_template('widgets/histogram.html',
            value=value, values=values, guids=guid_factory(), **kwargs)

