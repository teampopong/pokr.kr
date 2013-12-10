#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, render_template, request, send_file, url_for
from flask.ext.babel import gettext
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import desc

from cache import cache
from models.bill import Bill
from models.election import current_assembly_id
from utils.jinja import breadcrumb


def register(app):

    app.views['bill'] = 'bill_main'
    gettext('bill') # for babel extraction

    @app.route('/bill/', methods=['GET'])
    @breadcrumb(app)
    def bill_main():
        assembly_id = int(request.args.get('assembly_id', current_assembly_id()))
        bills = Bill.query.filter(Bill.age==assembly_id).order_by(desc(Bill.proposed_date).nullslast())
        return render_template('bills.html',\
                assembly_id=assembly_id, bills=bills)

    @app.route('/bill/<id>', methods=['GET'])
    @breadcrumb(app, 'bill')
    def bill(id):
        try:
            bill = Bill.query.filter_by(id=id).one()

        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('bill.html', bill=bill)

    @app.route('/bill/<id>/pdf', methods=['GET'])
    def bill_pdf(id):
        try:
            bill = Bill.query.filter_by(id=id).one()

        except NoResultFound, e:
            return render_template('not-found.html'), 404

        if bill.document_pdf_path:
            return send_file(bill.document_pdf_path)
        else:
            return render_template('not-found.html'), 404

    @app.route('/bill/<id>/text', methods=['GET'])
    def bill_text(id):
        try:
            bill = Bill.query.filter_by(id=id).one()

        except NoResultFound, e:
            return render_template('not-found.html'), 404

        if bill.document_text_path:
            glossary_js = generate_glossary_js()
            with open(bill.document_text_path) as f:
                response = render_template('bill-text.html', bill=bill, f=f,
                        glossary_js=glossary_js)
            return response
        else:
            return render_template('not-found.html'), 404


@cache.memoize(timeout=60*60*24)
def generate_glossary_js():
    terms_regex = open('./data/glossary-terms.regex').read().decode('utf-8').strip()
    dictionary = open('./data/glossary-map.json').read().decode('utf-8').strip()
    return render_template('js/glossary.js', terms_regex=terms_regex,
            dictionary=dictionary)

