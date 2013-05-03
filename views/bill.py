#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, render_template, request, url_for
from sqlalchemy.orm.exc import NoResultFound
from models.bill import Bill

def register(app):

    @app.route('/bill/', methods=['GET'])
    def bill_main():
        # TODO: 의안 목록 나오도록 수정
        return render_template('layout.html')

    @app.route('/bill/<id>', methods=['GET'])
    def bill(id):
        try:
            bill = Bill.query.filter_by(id=id).one()

        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('bill.html', bill=bill)

    # TODO: bill pdf route 만들기
    # TODO: bill text route 만들기
