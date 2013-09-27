#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import operator
import time

from flask import redirect, render_template, request, url_for
from flask.ext.babel import gettext
from sqlalchemy import and_
from sqlalchemy.orm import undefer_group
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import desc

from database import db_session
from models.assembly import Assembly, current_session_id
from models.candidacy import Candidacy
from models.election import Election
from models.person import Person
from utils.jinja import breadcrumb


def register(app):

    app.views['person'] = 'person_main'
    gettext('person') # for babel extraction

    person_names_json = json.dumps(all_person_names())

    # 루트
    @app.route('/person/', methods=['GET'])
    @breadcrumb(app)
    def person_main():
        # FIXME: 19
        session_id = current_session_id() or 0
        session_id = int(request.args.get('session_id', session_id))
        officials = Person.query.order_by(desc(Person.id))\
                                .join(Person.candidacies)\
                                .join(Candidacy.election)\
                                .join(Election.organization.of_type(Assembly))\
                                .filter(and_(Assembly.session_id == session_id,
                                             Candidacy.is_elected == True))

        return render_template('people.html',
                                officials=officials,
                                assembly_id=session_id) # FIXME assembly_id

    @app.route('/person/all-names.json', methods=['GET'])
    def person_all_names():
        return person_names_json

    # 사람
    @app.route('/person/<int:id>', methods=['GET'])
    @breadcrumb(app, 'person')
    def person(id):
        try:
            person = Person.query\
                           .filter_by(id=id)\
                           .options(undefer_group('extra'),
                                    undefer_group('profile'))\
                           .one()
        except NoResultFound, e:
            return render_template('not-found.html'), 404

        try:
            person_extra_vars = json.loads(person.extra_vars or '{}')
            if type(person_extra_vars.get('experience', None)) in [str, unicode]:
                person_extra_vars['experience'] = [person_extra_vars['experience']]
        except ValueError, e:
            pass

        return render_template('person.html', person=person,
                person_extra_vars=person_extra_vars)


def all_person_names():
    name_tuples = [list(i) for i in db_session.query(
        Person.name,
        Person.name_en,
        )]

    all_names = []
    if name_tuples:
        all_names = list(set(reduce(operator.add, name_tuples)))

    return all_names

