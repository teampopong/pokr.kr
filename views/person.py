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

from cache import cache
from database import db_session
from models.bill import Bill
from models.candidacy import Candidacy
from models.cosponsorship import cosponsorship
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
        assembly_id = int(request.args.get('assembly_id', 19))
        officials = Person.query.order_by(desc(Person.id))\
                                .join(Candidacy)\
                                .filter(and_(Candidacy.age == assembly_id,
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

    @app.route('/i/favorite/person/<int:id>', methods=['POST', 'DELETE'])
    def favorite_person(id):
        if not g.user.is_anonymous():
            update_favorite_person(id, request.method)
        return ''


def all_person_names():
    name_tuples = (list(i) for i in db_session.query(
        Person.name,
        Person.name_en,
        ))
    all_names = list(set(reduce(operator.add, name_tuples)))
    return all_names


def update_favorite_person(person_id, method):
    '''s: { 0: do not change
            1: set
            2: unset }
    '''
    try:
        person = Person.query.filter_by(id=person_id).one()
    except NoResultFound, e:
        abort(404)

    dirty = False
    if method.lower() == 'post':
        if person not in g.user.favorite_people:
            g.user.favorite_people.append(person)
            dirty = True
    elif method.lower() == 'delete':
        if person.id in (p.id for p in g.user.favorite_people):
            g.user.favorite_people.remove(person)
            dirty = True
    if dirty:
        db_session.commit()


@cache.memoize(timeout=60*60*4)
def distribution_of_cosponsorships(age):
    bill_t = Bill.__table__
    stmt = select([func.count(cosponsorship.c.id)])\
            .select_from(cosponsorship.join(bill_t))\
            .where(bill_t.c.age == age)\
            .group_by(cosponsorship.c.person_id)
    distribution = db_session.execute(stmt).fetchall()
    distribution = map(lambda x: x[0], distribution)
    return distribution
