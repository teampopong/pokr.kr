#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, render_template, request, url_for
from sqlalchemy.orm.exc import NoResultFound
from models.bill import Bill


PAGESIZE = 20


def register(app):

    @app.route('/bill/', methods=['GET'])
    def bill_main():
        bills = Bill.query.order_by(Bill.id)
        offset = int(request.args.get('offset', 0))
        return render_template('bills.html', bills=bills, offset=offset, pagesize=PAGESIZE)

    @app.route('/bill/<id>', methods=['GET'])
    def bill(id):
        try:
            bill = Bill.query.filter_by(id=id).one()

        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('bill.html', bill=bill)

    # TODO: bill pdf route 만들기
    # TODO: bill text route 만들기
