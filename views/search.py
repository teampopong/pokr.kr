from functools import wraps
from itertools import chain

from flask import request, render_template
from sqlalchemy import func, or_
from sqlalchemy.sql.expression import and_, desc, false
from werkzeug.local import LocalProxy

from models.cosponsorship import cosponsorship
from models.bill import Bill
from models.party import Party
from models.person import Person
from models.region import Region
from models.school import School
from models.query_log import log_query
from utils.jinja import breadcrumb


query = LocalProxy(lambda: request.args.get('query'))
target = LocalProxy(lambda: request.args.get('target'))


def register(app):

    @app.route('/search', methods=['GET'])
    @breadcrumb(app)
    def search():
        log_query(query)
        results, options = {}, {}
        results['people'] , options['people']  = search_people()
        results['parties'], options['parties'] = search_parties()
        results['schools'], options['schools'] = search_schools()
        results['bills']  , options['bills']   = search_bills()
        results['regions'], options['regions'] = search_regions()
        options = dict(chain(*(d.iteritems() for d in options.itervalues())))
        return render_template('search-results.html', option_texts=options, **results)


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

    @if_target('bills')
    def search_bills():
        options = {}
        person_id = request.args.get('person_id')
        assembly_id = request.args.get('assembly_id')

        bills = Bill.query.order_by(desc(Bill.proposed_date).nullslast())

        if query:
            bills = bills.filter(Bill.name.like(u'%{0}%'.format(query)))

        if person_id:
            bills = bills.join(cosponsorship)\
                         .join(Person)\
                         .filter(Person.id == person_id)
            options['person_id'] = Person.query.filter_by(id=person_id).one().name

        if assembly_id:
            bills = bills.filter(Bill.age == assembly_id)

        return (bills, options)

    @if_target('regions')
    def search_regions():
        options = {}
        regions = Region.query\
                        .filter(and_(
                                Region.name.like(u'%{0}%'.format(query)),
                                func.length(Region.id) < 7))
        return (regions, options)


def if_target(target_):
    def deco(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if target and target != target_:
                return (Party.query.filter(false()), {})
            return f(*args, **kwargs)
        return decorated
    return deco
