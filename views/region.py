#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, render_template, request, url_for
from sqlalchemy.orm.exc import NoResultFound

from models.region import Region


def register(app):

    @app.route('/region/', methods=['GET'])
    def region_main():
        regions = Region.query.order_by(Region.id)
        return render_template('regions.html', regions=regions)

    @app.route('/region/<region_id>', methods=['GET'])
    def region(region_id):
        try:
            region = Region.query.filter_by(id=region_id).one()
        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('region.html', region=region)
