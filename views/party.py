#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, render_template, request, url_for
from flask.ext.babel import gettext
from sqlalchemy import distinct
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
        #TODO: 외부에서 입력받기
        duplicates = [
            u'한국독립당',
            u'민중당',
            u'청년당',
            u'민주국민당',
            u'사회당',
            u'민주당',
            u'통일당',
            u'국민당',
            u'한국사회당',
            u'민주통일당',
            u'통합민주당']
        try:
            party = Party.query.filter_by(id=id).one()

        except NoResultFound, e:
            return render_template('not-found.html'), 404

        is_duplicate = party.name in duplicates
        candidacies = Candidacy.query\
                               .join(Party)\
                               .filter(Party.id == party.id)\
                               .distinct(Candidacy.age)
        assemblies = [candidacy.age for candidacy in candidacies]
        return render_template('party.html',\
                                party=party,\
                                is_duplicate=is_duplicate,\
                                assemblies=assemblies)
