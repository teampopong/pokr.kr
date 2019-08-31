#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from collections import defaultdict

from flask import redirect, render_template, request, url_for
from flask_babel import gettext
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import desc

from pokr.models.candidacy import Candidacy
from pokr.models.election import current_parliament_id
from pokr.models.party import Party
from utils.jinja import breadcrumb


def register(app):

    app.views['party'] = 'party_main'
    gettext('party') # for babel extraction

    # 루트
    @app.route('/party/', methods=['GET'])
    @breadcrumb(app)
    def party_main():
        election_type = request.args.get('election_type', 'assembly')
        assembly_id = int(request.args.get('assembly_id', current_parliament_id(election_type)) or 0)

        parties = Party.query\
                        .join(Candidacy)\
                        .filter(Candidacy.assembly_id == assembly_id)\
                        .filter(Candidacy.type == election_type)\
                        .group_by(Party.id)\
                        .order_by(func.count().desc())

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

        except NoResultFound as e:
            return render_template('not-found.html'), 404

        is_duplicate = party.name in duplicates
        candidacies = Candidacy.query\
                               .join(Party)\
                               .filter(Party.id == party.id)\
                               .distinct(Candidacy.type, Candidacy.assembly_id)
        elections = defaultdict(list)
        for candidacy in candidacies:
            elections[candidacy.type].append(candidacy.assembly_id)
        return render_template('party.html',\
                                party=party,\
                                is_duplicate=is_duplicate,\
                                elections=elections)
