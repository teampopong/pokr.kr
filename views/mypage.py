#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import g, redirect, render_template, url_for
from flask.ext.babel import gettext
from sqlalchemy.sql.expression import or_

from models.bill import Bill
from models.bill_feed import BillFeed
from models.feed import Feed
from models.keyword import Keyword
from models.person import Person
from utils.jinja import breadcrumb


def register(app):

    app.views['mypage'] = 'mypage'

    @app.route('/mypage/', methods=['GET'])
    @breadcrumb(app)
    def mypage():
        if g.user.is_anonymous():
            return redirect(url_for('login'))

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

        return render_template('mypage.html', feeds=feeds)

