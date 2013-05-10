#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import render_template


def register(app):

    @app.route('/region/', methods=['GET'])
    def region_main():
        return render_template('region.html')

    @app.route('/region/<id>', methods=['GET'])
    def region(id):
        return render_template('region.html', id=id)

