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

    @app.route('/region/', methods=['GET'])
    @breadcrumb(app)
    def region_main():
        provinces = Region.query.filter(func.length(Region.id) == 2)
        return render_template('regions.html', provinces=provinces)

    @app.route('/region/<region_id>', methods=['GET'])
    @breadcrumb(app, 'region')
    def region(region_id):
        try:
            region = Region.query.filter_by(id=region_id).one()
        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('region.html', region=region)

    @app.route('/find-region')  # FIXME: change url
    def find_region():
        q = request.args.get('query', '')
        regions = Region.query.filter(Region.name.like(u'%{0}%'.format(q)))
        return render_template('region-list.html', regions=regions)

