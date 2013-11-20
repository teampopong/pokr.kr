#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import g, redirect, render_template, request, url_for
from flask.ext.babel import gettext
from sqlalchemy.sql.expression import or_

from models.bill import Bill
from models.bill_feed import BillFeed
from models.feed import Feed
from models.keyword import Keyword
from models.person import Person
from utils.jinja import breadcrumb, jsonify
from utils.paginate import MoreQuery


def register(app):

    app.views['mypage'] = 'mypage'

    more = MoreQuery(Feed, 'mypage_feeds', 'desc', 'feeds')

    @app.route('/mypage/', methods=['GET'])
    @breadcrumb(app)
    def mypage():
        if g.user.is_anonymous():
            return redirect(url_for('login'))

        data = more.query(my_feeds())
        return render_template('mypage.html', **data)

    @app.route('/mypage/feeds', methods=['GET'])
    def mypage_feeds():
        if g.user.is_anonymous():
            return redirect(url_for('login'))

        data = more.query(my_feeds(), _from=request.args.get('before', None))
        data['html'] = render_template('feeds.html', **data)
        del data['feeds']
        return jsonify(data)


def my_feeds():
    feeds = Feed.query\
                .with_polymorphic('*')\
                .join(BillFeed.bill)\
                .outerjoin(Bill.cosponsors)\
                .outerjoin(Bill.keywords)\
                .filter(or_(
                    Keyword.id.in_(k.id for k in g.user.favorite_keywords),
                    Person.id.in_(p.id for p in g.user.favorite_people),
                ))\
                .order_by(Feed.id.desc())
    return feeds

