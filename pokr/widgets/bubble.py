# -*- coding: utf-8 -*-

from flask import render_template

from utils.jinja import guid_factory


def bubble(items, diameter=500):
    return render_template('widgets/bubble.html', items=items,\
            diameter=diameter, guids=guid_factory())
