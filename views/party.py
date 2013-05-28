#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, render_template, request, url_for
from flask.ext.babel import gettext
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import desc

from models.candidacy import Candidacy
from models.party import Party
from utils.jinja import breadcrumb


def register(app):

    app.views['party'] = 'party_main'
    gettext('party') # for babel extraction

    # 루트
    @app.route('/party/', methods=['GET'])
    @breadcrumb(app)
    def party_main():
        # FIXME: 19
        assembly_id = int(request.args.get('assembly_id', 19))

        parties = Party.query.distinct(Party.id)\
                        .join(Candidacy)\
                        .filter(Candidacy.age==assembly_id)

        return render_template('parties.html',\
                                assembly_id=assembly_id,\
                                parties=parties)

    # 이름으로 검색
    @app.route('/party/<id>', methods=['GET'])
    @breadcrumb(app, 'party')
    def party(id):
        try:
            party = Party.query.filter_by(id=id).one()

        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('party.html', party=party)
