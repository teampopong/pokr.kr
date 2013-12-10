# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

from controllers.base import Controller
from models.bill import Bill
from models.candidacy import Candidacy
from models.cosponsorship import cosponsorship
from models.person import Person
from models.pledge import Pledge


class PersonController(Controller):
    model = 'person'

    @classmethod
    def bills_of(cls, person, age=None):
        query = Bill.query.join(cosponsorship,
                                Bill.id == cosponsorship.c.bill_id)\
                          .join(Person,
                                Person.id == cosponsorship.c.person_id)\
                          .filter_by(id=person.id)\
                          .order_by(Bill.proposed_date.desc())
        if age:
            query = query.filter(Bill.age == age)

        return query

    @classmethod
    def keyword_counts(cls, person, limit=10):
        # TODO: batch calculation or non-blocking operation
        elected_assembly_ids = [candidacy.age for candidacy in person.candidacies if candidacy.is_elected]

        if not elected_assembly_ids:
            return {}

        latest_assembly_id = max(elected_assembly_ids)
        keywords = (keyword.name
                        for bill in cls.bills_of(person, latest_assembly_id)
                        for keyword in bill.keywords)
        counter = Counter(keywords)

        return dict(counter.most_common(limit))

    @classmethod
    def party_history(cls, person):
        parties_and_ages = person.parties.add_columns(Candidacy.age)
        result = []
        prev_party_id = None
        for party, age in parties_and_ages:
            if prev_party_id == party.id:
                result[-1][0].append(age)
            else:
                result.append(([age], party))
                prev_party_id = party.id
        return [(party, min(ages), max(ages)) for ages, party in result]

    @classmethod
    def pledges_grouped_by_age(cls, person):
        query = Pledge.query.join(Candidacy,
                                  Candidacy.id == Pledge.candidacy_id)\
                            .join(Person,
                                  Person.id == Candidacy.person_id)\
                            .filter(Person.id == person.id)\
                            .order_by(Pledge.id)

        result = defaultdict(list)
        for pledge in query:
            result[pledge.candidacy.age].append(pledge)

        return result

