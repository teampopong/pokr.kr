#!/usr/bin/env python

from flask import Blueprint, redirect, url_for

app = Blueprint('main', __name__)

@app.route('/')
def main():
    return redirect(url_for('people.main'))

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('images/favicon.ico')
