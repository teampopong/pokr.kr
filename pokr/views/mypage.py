#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import abort, g, redirect, render_template, request, url_for
from flask.ext.babel import gettext
from popong_models.region import Region
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import or_

from pokr.models.feed import Feed
from pokr.models.user import User
from utils.jinja import breadcrumb, jsonify
from utils.paginate import MoreQuery


def register(app):

    app.views['mypage'] = 'mypage'

    keyword_more = MoreQuery(Feed, 'keyword_feeds', 'desc', 'feeds')
    district_more = MoreQuery(Feed, 'district_feeds', 'desc', 'feeds')

    @app.route('/i', methods=['GET'])
    @breadcrumb(app)
    def mypage():
        if g.user.is_anonymous():
            abort(401)

        legislator = Region.legislator_of(g.user.address_id)
        district_feeds = User.district_feeds(legislator)
        district_feeds = district_more.query(district_feeds)
        keyword_feeds = g.user.keyword_feeds()
        keyword_feeds = keyword_more.query(keyword_feeds)
        return render_template('mypage.html',
                legislator=legislator,
                district_feeds=district_feeds,
                keyword_feeds=keyword_feeds)

    @app.route('/i/feeds/district', methods=['GET'])
    def district_feeds():
        if g.user.is_anonymous():
            abort(401)

        legislator = Region.legislator_of(g.user.address_id)
        district_feeds = User.district_feeds(legislator)
        district_feeds = district_more.query(district_feeds,  _from=request.args.get('before', None))
        district_feeds['html'] = render_template('district-feeds.html',
                legislator=legislator,
                district_feeds=district_feeds)
        del district_feeds['feeds']
        return jsonify(district_feeds)

    @app.route('/i/feeds/keyword', methods=['GET'])
    def keyword_feeds():
        if g.user.is_anonymous():
            abort(401)

        keyword_feeds = g.user.keyword_feeds()
        keyword_feeds = keyword_more.query(keyword_feeds,  _from=request.args.get('before', None))
        keyword_feeds['html'] = render_template('keyword-feeds.html', keyword_feeds=keyword_feeds)
        del keyword_feeds['feeds']
        return jsonify(keyword_feeds)

    @app.route('/i/person/<int:id>', methods=['POST', 'DELETE'])
    def favorite_person(id):
        if not g.user.is_anonymous():
            try:
                g.user.update_favorite_person(id, request.method)
            except NoResultFound as e:
                abort(404)
        return ''

    @app.route('/i/keyword/<keyword>', methods=['POST', 'DELETE'])
    def favorite_keyword(keyword):
        if not g.user.is_anonymous():
            try:
                g.user.update_favorite_keyword(keyword, request.method)
            except NoResultFound as e:
                abort(404)
        return ''

    @app.route('/i/region', methods=['PUT'])
    def update_address():
        region_id = request.form.get('region_id')

        if not region_id:
            abort(404)

        g.user.update_address(region_id)
        return ''

