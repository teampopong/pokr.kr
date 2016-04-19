# -*- coding: utf-8 -*-

import re
import regex
from functools import wraps
from itertools import chain

from flask import request, render_template
from sqlalchemy import func, or_
from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import and_, desc, false
from werkzeug.local import LocalProxy

from pokr.models.cosponsorship import cosponsorship
from pokr.models.bill import Bill
from pokr.models.bill_status import BillStatus
from pokr.models.keyword import Keyword
from pokr.models.meeting import Meeting
from pokr.models.party import Party
from pokr.models.person import Person
from pokr.models.region import Region
from pokr.models.school import School
from pokr.models.statement import Statement
from pokr.models.query_log import log_query
from utils.jinja import breadcrumb


query = LocalProxy(lambda: request.args.get('query'))
target = LocalProxy(lambda: request.args.get('target'))


def register(app):

    @app.route('/search', methods=['GET'])
    @breadcrumb(app)
    def search():
        log_query(query)

        results, options = {}, {}
        try:
            results['people'] , options['people']  = search_people()
            results['parties'], options['parties'] = search_parties()
            results['schools'], options['schools'] = search_schools()
            results['laws'], options['laws'] = search_laws()
            results['bills']  , options['bills']   = search_bills()
            results['regions'], options['regions'] = search_regions()
            results['meetings'], options['meetings'] = search_meetings()
            results['statements'], options['statements'] = search_statements()

            options = dict(chain(*(d.iteritems() for d in options.itervalues())))
            response = render_template('search-results.html',
                    option_texts=options, **results)
        except (DataError, NoResultFound) as e:
            # When such given *_id is invalid
            response = (render_template('not-found.html'), 404)

        return response


    @if_target('people')
    def search_people():
        options = {}
        school_id = request.args.get('school_id')
        party_id = request.args.get('party_id')
        candidacy_region_id = request.args.get('candidacy_region_id')
        residence_region_id = request.args.get('residence_region_id')
        if school_id:
            school = School.query.filter_by(id=school_id).one()
            options['school_id'] = school.name
            people = Person.query.join(School.alumni)\
                                 .filter(School.id == school_id)
        elif candidacy_region_id:
            region = Region.query.filter_by(id=candidacy_region_id).one()
            options['candidacy_region_id'] = region.fullname
            people = region.candidates
        elif residence_region_id:
            region = Region.query.filter_by(id=residence_region_id).one()
            options['residence_region_id'] = region.fullname
            people = region.residents
        elif party_id:
            party = Party.query.filter_by(id=party_id).one()
            options['party_id'] = party.name
            people = party.members
        else:
            people = Person.query

        if query:
            people = people.filter(or_(
                     Person.name.like(u'%{0}%'.format(query)),
                     Person.name_en.ilike(u'%{0}%'.format(query))
                 ))

        year = request.args.get('year')
        if year:
            people = people.filter_by(birthday_year=year)

        return (people, options)


    @if_target('parties')
    def search_parties():
        options = {}
        parties = Party.query
        if query:
            parties = parties.filter(Party.name.like(u'%{0}%'.format(query)))
        return (parties, options)

    @if_target('schools')
    def search_schools():
        options = {}
        schools = School.query
        if query:
            schools = schools.filter(School.name.like(u'%{0}%'.format(query)))
        return (schools, options)

    @if_target('laws')
    def search_laws():
        def strip_bill(bill):
            stripped = re.sub(u'\(대안\)', '', bill.name)
            replaced = stripped.replace(u'ㆍ', '')
            hanguls = regex.findall(ur'[\p{Hangul}]+', replaced.strip())
            billname = re.sub(u'중개정법률안', '', ''.join(hanguls))
            billname = re.sub(u'개정법률안', '', billname)
            billname = re.sub(ur'(일|전)부', '', billname)
            billname = billname.strip(u'안')
            return billname

        options = {}
        bills, options = search_bills()
        query = request.args.get('query')
        if query:
            bills = Bill.query.order_by(desc(Bill.proposed_date).nullslast())\
                    .filter(or_(
                        Bill.name.like(u'%{0}%'.format(query)),
                        Bill.keywords.any(Keyword.name==unicode(query))
                        ))
        laws = sorted(list(set([strip_bill(bill) for bill in bills])))
        return (laws, options)

    @if_target('bills')
    def search_bills():
        options = {}
        person_id = request.args.get('person_id')
        assembly_id = request.args.get('assembly_id')
        status_id = request.args.get('status_id')
        keyword_id = request.args.get('keyword_id')

        bills = Bill.query.order_by(desc(Bill.proposed_date).nullslast())

        if query:
            bills = bills.filter(or_(
                Bill.name.like(u'%{0}%'.format(query)),
                Bill.keywords.any(Keyword.name==unicode(query))
                ))

        if person_id:
            bills = bills.join(cosponsorship)\
                         .join(Person)\
                         .filter(Person.id == person_id)
            options['person_id'] = Person.query.filter_by(id=person_id).one().name

        if assembly_id:
            bills = bills.filter(Bill.assembly_id == assembly_id)

        if status_id:
            bills = bills.filter(Bill.status_id == status_id)
            options['status_id'] = BillStatus.query.filter_by(id=status_id).one().name

        if keyword_id:
            bills = bills.join(Bill.keywords)\
                         .filter(Keyword.id == keyword_id)
            options['keyword_id'] = Keyword.query.filter_by(id=keyword_id).one().name

        return (bills, options)

    @if_target('regions')
    def search_regions():
        options = {}
        regions = Region.query\
                        .filter(and_(
                                Region.name.like(u'%{0}%'.format(query)),
                                func.length(Region.id) < 7))
        return (regions, options)

    @if_target('meetings')
    def search_meetings():
        options = {}
        query = request.args.get('query')
        if query:
            meetings = Meeting.query\
                        .filter(Meeting.committee.like(u'%{0}%'.format(query)))\
                        .group_by(Meeting.id).order_by(desc(Meeting.date))
        return (meetings, options)

    @if_target('statements')
    def search_statements():
        options = {}
        person_id = request.args.get('person_id')

        statements = Statement.query.join(Meeting)\
                        .order_by(Meeting.date.desc().nullslast(),\
                                  Statement.sequence)

        if query:
            statements = statements\
                        .filter(Statement.content.like(u'%{0}%'.format(query)))

        if person_id:
            statements = statements.filter(Statement.person_id==person_id)
            options['person_id'] =\
                    Person.query.filter_by(id=person_id).one().name

        return (statements, options)


def if_target(target_):
    def deco(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if target and target != target_:
                return (Party.query.filter(false()), {})
            return f(*args, **kwargs)
        return decorated
    return deco
