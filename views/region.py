#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, render_template, request, url_for
from flask.ext.babel import gettext
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from models.region import Region
from utils.jinja import breadcrumb


def register(app):

    app.views['region'] = 'region_main'
    gettext('region') # for babel extraction

    with app.open_resource('static/images/korea_130_v3.1.svg') as f:
        korean_map = f.read().decode('utf-8')

    top_regions = Region.query\
                        .filter(func.length(Region.id) < 6)\
                        .order_by(Region.id).all()

    @app.route('/region/', methods=['GET'])
    @breadcrumb(app)
    def region_main():
        return render_template('regions.html', regions=top_regions,
                korean_map=korean_map)

    @app.route('/region/<region_id>', methods=['GET'])
    @breadcrumb(app, 'region')
    def region(region_id):
        try:
            region = Region.query.filter_by(id=region_id).one()
        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('region.html', region=region)

