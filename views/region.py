#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, render_template, request, url_for
from flask.ext.babel import gettext
from sqlalchemy.orm.exc import NoResultFound

from models.region import Region
from utils.jinja import breadcrumb


def register(app):

    @app.route('/region/', methods=['GET'])
    @breadcrumb(app)
    def region_main():
        regions = Region.query.order_by(Region.id)
        return render_template('regions.html', regions=regions)

    @app.route('/region/<region_id>', methods=['GET'])
    @breadcrumb(app, (gettext('region'), 'region_main', None))
    def region(region_id):
        try:
            region = Region.query.filter_by(id=region_id).one()
        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('region.html', region=region)
