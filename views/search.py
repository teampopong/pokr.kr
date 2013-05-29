from functools import wraps

from flask import request, render_template
from sqlalchemy import or_
from sqlalchemy.sql.expression import desc, false
from werkzeug.local import LocalProxy

from models.cosponsorship import cosponsorship
from models.bill import Bill
from models.party import Party
from models.person import Person
from models.region import Region
from models.school import School
from utils.jinja import breadcrumb


query = LocalProxy(lambda: request.args.get('query'))
target = LocalProxy(lambda: request.args.get('target'))


def register(app):

    @app.route('/search', methods=['GET'])
    @breadcrumb(app)
    def search():
        results = {}
        results['people'] = search_people()
        results['parties'] = search_parties()
        results['schools'] = search_schools()
        results['bills'] = search_bills()
        results['regions'] = search_regions()
        return render_template('search-results.html', **results)


    @if_target('people')
    def search_people():
        school_id = request.args.get('school_id')
        candidacy_region_id = request.args.get('candidacy_region_id')
        residence_region_id = request.args.get('residence_region_id')
        if school_id:
            school = School.query.filter_by(id=school_id).one()
            people = school.alumni
        elif candidacy_region_id:
            region = Region.query.filter_by(id=candidacy_region_id).one()
            people = region.candidates
        elif residence_region_id:
            region = Region.query.filter_by(id=residence_region_id).one()
            people = region.residents
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


        return people


    @if_target('parties')
    def search_parties():
        parties = Party.query
        if query:
            parties = parties.filter(Party.name.like(u'%{0}%'.format(query)))
        return parties

    @if_target('schools')
    def search_schools():
        schools = School.query
        if query:
            schools = schools.filter(School.name.like(u'%{0}%'.format(query)))
        return schools

    @if_target('bills')
    def search_bills():
        person_id = request.args.get('person_id')
        assembly_id = request.args.get('assembly_id')

        bills = Bill.query.order_by(desc(Bill.proposed_date))

        if query:
            bills = bills.filter(Bill.name.like(u'%{0}%'.format(query)))

        if person_id:
            bills = bills.join(cosponsorship)\
                         .join(Person)\
                         .filter(Person.id == person_id)

        if assembly_id:
            bills = bills.filter(Bill.age == assembly_id)

        return bills

    @if_target('regions')
    def search_regions():
        regions = Region.query.filter(Region.name.like(u'%{0}%'.format(query)))
        return regions


def if_target(target_):
    def deco(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if target and target != target_:
                return Party.query.filter(false())
            return f(*args, **kwargs)
        return decorated
    return deco
