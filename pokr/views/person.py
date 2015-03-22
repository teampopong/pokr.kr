#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import operator
import time

from flask import abort, current_app, g, redirect, render_template, request, url_for
from flask.ext.babel import gettext
from sqlalchemy import and_, func
from sqlalchemy.orm import undefer_group
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import select, desc

from pokr.cache import cache
from pokr.database import db_session
from pokr.models.bill import Bill
from pokr.models.candidacy import Candidacy
from pokr.models.cosponsorship import cosponsorship
from pokr.models.election import current_parliament_id
from pokr.models.person import Person
from utils.jinja import breadcrumb


def register(app):

    app.views['person'] = 'person_main'
    gettext('person') # for babel extraction

    person_names_json = json.dumps(all_person_names())

    # 루트
    @app.route('/person/', methods=['GET'])
    @breadcrumb(app)
    def person_main():
        sort = request.args.get('sort', 'name')
        election_type = request.args.get('election_type', 'assembly')
        assembly_id = int(request.args.get('assembly_id', current_parliament_id(election_type)) or 0)

        if sort == 'cosponsorship':
            bill_t = Bill.__table__
            cosponsorship_count = db_session.query(
                        cosponsorship.c.person_id,
                        func.count(cosponsorship.c.id).label('cosponsorship_count')
                    )\
                .outerjoin(bill_t)\
                .filter(bill_t.c.assembly_id == assembly_id)\
                .group_by(cosponsorship.c.person_id)\
                .subquery('cosponsorship_count')

            officials = Person.query.order_by(
                                            desc(func.coalesce(func.sum(cosponsorship_count.c.cosponsorship_count), 0))
                                        )\
                                    .join(Candidacy)\
                                    .outerjoin(cosponsorship_count)\
                                    .filter(and_(Candidacy.type == election_type,
                                                 Candidacy.assembly_id == assembly_id,
                                                 Candidacy.is_elected == True))\
                                    .group_by(Person.id)
        else:
            officials = Person.query.order_by(Person.name)\
                                    .join(Candidacy)\
                                    .filter(and_(Candidacy.type == election_type,
                                                 Candidacy.assembly_id == assembly_id,
                                                 Candidacy.is_elected == True))

        return render_template('people.html',
                                officials=officials,
                                assembly_id=assembly_id)

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
                distribution_of_cosponsorships=distribution_of_cosponsorships,
                person_extra_vars=person_extra_vars)


def all_person_names():
    name_tuples = (list(i) for i in db_session.query(
        Person.name,
        Person.name_en,
        ))
    all_names = ''
    try:
        all_names = list(set(reduce(operator.add, name_tuples)))
    except TypeError as e:
        pass
    return all_names


@cache.memoize(timeout=60*60*4)
def distribution_of_cosponsorships(assembly_id):
    bill_t = Bill.__table__
    stmt = select([func.count(cosponsorship.c.id)])\
            .select_from(cosponsorship.join(bill_t))\
            .where(bill_t.c.assembly_id == assembly_id)\
            .group_by(cosponsorship.c.person_id)
    distribution = db_session.execute(stmt).fetchall()
    distribution = map(lambda x: x[0], distribution)
    return distribution
