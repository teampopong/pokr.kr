#!/usr/bin/env python

from flask import Blueprint, current_app

app = Blueprint('figures', __name__)

@app.route('/')
def figures():
    # can use current_app.db, current_app.cache
    return ''
