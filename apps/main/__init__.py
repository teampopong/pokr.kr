#!/usr/bin/env python

from flask import Blueprint, redirect, url_for

app = Blueprint('main', __name__)

@app.route('/')
def main():
    return redirect(url_for('people.main'))
