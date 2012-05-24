#!/usr/bin/env python

from flask import Blueprint, current_app

polidic = Blueprint('polidic', __name__)

@polidic.route('/')
def members():
    # can use current_app.db, current_app.cache
    return ''
