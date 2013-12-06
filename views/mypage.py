#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import abort, g, redirect, render_template, request, url_for
from flask.ext.babel import gettext
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import or_

from controllers.user import UserController
from database import db_session
from models.feed import Feed
from utils.jinja import breadcrumb, jsonify
from utils.paginate import MoreQuery


def register(app):

    app.views['mypage'] = 'mypage'

    more = MoreQuery(Feed, 'keyword_feeds', 'desc', 'feeds')

    @app.route('/i', methods=['GET'])
    @breadcrumb(app)
    def mypage():
        if g.user.is_anonymous():
            abort(401)

        keyword_feeds = UserController.keyword_feeds(g.user)
        keyword_feeds = more.query(keyword_feeds)
        return render_template('mypage.html', keyword_feeds=keyword_feeds)

    @app.route('/i/feeds/keyword', methods=['GET'])
    def keyword_feeds():
        if g.user.is_anonymous():
            abort(401)

        keyword_feeds = UserController.keyword_feeds(g.user)
        keyword_feeds = more.query(keyword_feeds,  _from=request.args.get('before', None))
        keyword_feeds['html'] = render_template('keyword-feeds.html', keyword_feeds=keyword_feeds)
        del keyword_feeds['feeds']
        return jsonify(keyword_feeds)

    @app.route('/i/person/<int:id>', methods=['POST', 'DELETE'])
    def favorite_person(id):
        if not g.user.is_anonymous():
            try:
                UserController.update_favorite_person(g.user, id,
                        request.method)
            except NoResultFound as e:
                abort(404)
        return ''

    @app.route('/i/keyword/<keyword>', methods=['POST', 'DELETE'])
    def favorite_keyword(keyword):
        if not g.user.is_anonymous():
            try:
                UserController.update_favorite_keyword(g.user, keyword,
                        request.method)
            except NoResultFound as e:
                abort(404)
        return ''

