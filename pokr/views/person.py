#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import operator
import time
from collections import defaultdict

from flask import abort, current_app, g, jsonify, redirect, render_template, request, url_for
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
from pokr.models.party import Party
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
        election_type = request.args.get('election_type', 'assembly')
        assembly_id = int(request.args.get('assembly_id', current_parliament_id(election_type)) or 0)
        view_type = request.args.get('type', 'list')

        if view_type=='card':
            officials = Person.query.order_by(Person.name)\
                                .join(Candidacy)\
                                .filter(and_(Candidacy.type==election_type,
                                             Candidacy.assembly_id==assembly_id,
                                             Candidacy.is_elected==True))
            return render_template('people-card.html',
                                    officials=officials,
                                    assembly_id=assembly_id)

        else:  # default
            return render_template('people-list.html',
                                    assembly_id=assembly_id)

    @app.route('/person/all-names.json', methods=['GET'])
    def person_all_names():
        return person_names_json


    @app.route('/person/list', methods=['GET'])
    def people_list():

        def wrap(data):
            return [{
                'DT_RowId': d.id,
                'DT_RowClass': 'clickable',
                'image': '<img src="%s" width="30px" height="40px">' % d.image,
                'name': d.name,
                'gender': '여' if d.gender=='f' else '남',
                'birthday': d.birthday_year,
                'cur_party': d.cur_party.name,
                'nelected': d.nelected
                } for d in data]

        election_type = request.args.get('election_type', 'assembly')
        assembly_id = int(\
                request.args.get('assembly_id', current_parliament_id(election_type)) or 0)

        draw = int(request.args.get('draw', 1))  # iteration number
        start = int(request.args.get('start', 0))  # starting row's id
        length = int(request.args.get('length', 10))  # number of rows in page

        # order by
        columns = ['image', 'name', 'gender', 'birthday', 'cur_party', 'nelected']
        if draw==1:
            order_column = func.random()  # shuffle rows
        elif request.args.get('order[0][column]'):
            order_column = columns[int(request.args.get('order[0][column]'))]
            if request.args.get('order[0][dir]', 'asc')=='desc':
                order_column += ' desc'
        else:
            order_column = None

        officials = Person.query.join(Candidacy)\
                                .filter(and_(Candidacy.type==election_type,
                                             Candidacy.assembly_id==assembly_id,
                                             Candidacy.is_elected==True))\
                                .order_by(order_column)

        filtered = officials.offset(start).limit(length)

        response = {
            'draw': draw,
            'data': wrap(filtered),
            'recordsTotal': officials.count(),
            'recordsFiltered': officials.count()
        }
        return jsonify(**response)


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
