#!/usr/bin/env python

from flask import Blueprint, render_template

app = Blueprint('main', __name__, template_folder='templates')

@app.route('/')
def main():
    return render_template('main.html', menu='home')
