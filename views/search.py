from flask import request, render_template
from sqlalchemy import or_
from sqlalchemy.sql.expression import desc

from models.cosponsorship import cosponsorship
from models.bill import Bill
from models.party import Party
from models.person import Person
from models.region import Region
from models.school import School
from utils.jinja import breadcrumb

def register(app):

    @app.route('/search/<query>', methods=['GET'])
    @app.route('/search', methods=['GET'])
    @breadcrumb(app)
    def search(query=''):
        target = request.args.get('target')
        if not target:
            return search_all(query)
        elif target == 'bill':
            return search_bills(query)

        raise Exception('Unknown target')


    def search_all(query):
        year = request.args.get('year')
        query = query or request.args.get('query')

        if query:
            people = Person.query.filter(or_(
                         Person.name.like(u'%{0}%'.format(query)),
                         Person.name_en.ilike(u'%{0}%'.format(query))
                     ))
            parties = Party.query.filter(Party.name.like(u'%{0}%'.format(query)))
            schools = School.query.filter(School.name.like(u'%{0}%'.format(query)))
            bills = Bill.query.filter(Bill.name.like(u'%{0}%'.format(query)))
            regions = Region.query.filter(Region.name.like(u'%{0}%'.format(query)))

        if year:
            if 'people' not in locals():
                people = Person.query
            people = people.filter_by(birthday_year=year)

        return render_template('search-results.html', **locals())


    def search_bills(query):
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

        return render_template('bills.html', bills=bills)
