# -*- coding: utf-8 -*-
import math
import numpy

from collections import Counter, defaultdict, OrderedDict

from .base import Controller
from pokr.cache import cache
from pokr.database import db_session
from pokr.models import Bill, Candidacy, cosponsorship, Meeting, Party, Person, Pledge, Statement
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import select

class PersonController(Controller):
    model = 'person'

    @classmethod
    def allies(cls, person, assembly_id=None, threshold=0.5):
        bills = cls.bills_of(person, assembly_id)
        sponsored_bills = (bill for bill in bills if person.id in (p.id for p in bill.representative_people))
        counter = Counter()
        num_sponsored_bills = 0
        for bill in bills:
            followers = db_session.query(Person.id)\
                              .join(cosponsorship)\
                              .filter(cosponsorship.c.bill_id == bill.id)
            counter = counter + Counter(follower.id for follower in followers if follower.id != person.id)
            num_sponsored_bills += 1

        return OrderedDict(
            (key, (value + .0) / num_sponsored_bills)
                for key, value in counter.most_common(10)\
                if (value + .0) / num_sponsored_bills > threshold
        )

    @classmethod
    def bills_of(cls, person, assembly_id=None):
        query = Bill.query.join(cosponsorship,
                                Bill.id == cosponsorship.c.bill_id)\
                          .join(Person,
                                Person.id == cosponsorship.c.person_id)\
                          .filter_by(id=person.id)\
                          .order_by(Bill.proposed_date.desc())
        if assembly_id:
            query = query.filter(Bill.assembly_id == assembly_id)

        return query

    @classmethod
    def keyword_counts(cls, person, limit=10):
        # TODO: batch calculation or non-blocking operation
        elected_assembly_ids = [candidacy.assembly_id for candidacy in person.candidacies if candidacy.is_elected]

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
        parties_and_assembly_ids = Party.query\
                                        .join(Candidacy)\
                                        .filter(Candidacy.person_id == person.id)\
                                        .join(Person)\
                                        .order_by(Candidacy.election_date.desc())\
                                        .add_columns(Candidacy.type, Candidacy.assembly_id)
        result = []
        prev_party_id = None
        for party, election_type, assembly_id in parties_and_assembly_ids:
            # TODO: 국회의원 선거 외 다른 선거도.
            if election_type != 'assembly':
                continue
            if prev_party_id == party.id:
                result[-1][0].append(assembly_id)
            else:
                result.append(([assembly_id], party))
                prev_party_id = party.id
        return [(party, min(assembly_ids), max(assembly_ids)) for assembly_ids, party in result]

    @classmethod
    def pledges_grouped_by_assembly_id(cls, person):
        query = Pledge.query.join(Candidacy,
                                  Candidacy.id == Pledge.candidacy_id)\
                            .join(Person,
                                  Person.id == Candidacy.person_id)\
                            .filter(Person.id == person.id)\
                            .order_by(Pledge.id)

        result = defaultdict(list)
        for pledge in query:
            result[pledge.candidacy.assembly_id].append(pledge)

        return result

    @classmethod
    def sorted_statements(cls, person):
        return Statement.query.join(Meeting)\
                  .filter(Statement.person_id==person.id)\
                  .order_by(Meeting.date.desc().nullslast(), Statement.sequence)

    @classmethod
    def get_similar_assembly_members(cls, person, assembly_id):
        ideology_tuples = calculate_ideology_tuple(assembly_id)
        # find the person's ideology level
        self_ideology_tuple = None
        for ideology_tuple in ideology_tuples:
            if ideology_tuple[0] == person.id:
                self_ideology_tuple = ideology_tuple
                break

        #remove self from the tuples
        ideology_tuples.remove(self_ideology_tuple)
        self_ideology = self_ideology_tuple[1]

        # find the most similar 5 persons
        diff_ideology_tuples = map(lambda tuple: (tuple[0], math.fabs(tuple[1] - self_ideology)), ideology_tuples)
        diff_ideology_tuples.sort(cmp=lambda x,y: cmp(x[1], y[1]))
        similar_people_ids = map(lambda tuple: tuple[0], diff_ideology_tuples[:5])

        return Person.query\
          .filter(Person.id.in_(similar_people_ids))\
          .all()



def rescale(u):
    u = (u - min(u)) / (max(u) - min(u))
    return [float(v) for v in u]

# Also draws heavily from govtrack.us
@cache.memoize(timeout=60*60*24)
def generate_cosponsorship_matrix(assembly_id):
    try:
        bills = Bill.query.filter(Bill.assembly_id==assembly_id).all()
        rep_to_row = {}
        cosponsorships = []

        def rownum(id):
            if not id in rep_to_row:
                rep_to_row[id] = len(rep_to_row)
            return rep_to_row[id]

        for bill in bills:
            reps = bill.representative_people
            if len(reps) == 0:
                continue

            for rep in reps:
                for cosponsor in bill.cosponsors:
                    rownum(cosponsor.id)
                    cosponsorships.append((rep.id, cosponsor.id))

        P = numpy.identity(len(rep_to_row), numpy.float)
        for sponsor, cosponsor in cosponsorships:
            P[rep_to_row[sponsor], rep_to_row[cosponsor]] += 1.0

    except NoResultFound, e:
        print e

    return rep_to_row, P

# Got a lot of inspiration from govtrack.us
@cache.memoize(timeout=60*60*24)
def calculate_ideology_tuple(assembly_id):
    try:
        rep_to_row, P = generate_cosponsorship_matrix(assembly_id)
        u, s, vh = numpy.linalg.svd(P)
        spectrum = vh[1,:]
        spectrum = rescale(spectrum)
        ids = [None for k in rep_to_row]
        for k, v in rep_to_row.items():
            ids[v] = k

        ideology_tuples = []
        for index, person_id in enumerate(ids):
            ideology_tuples.append((person_id, spectrum[index]))

        ideology_tuples.sort(cmp=lambda x,y: cmp(x[1], y[1]))

    except NoResultFound, e:
        print e

    return ideology_tuples
