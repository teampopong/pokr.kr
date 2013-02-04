# -*- coding: utf-8 -*-

from collections import defaultdict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from models.candidacy import Candidacy
from models.election import Election
from models.party import Party
from models.person import Person
from models.party import Party
from utils.mongodb import mongodb

__all__ = ['create_db', 'migrate_all']

# db connections
engine = create_engine('DRIVER_HERE://ID_HERE:PWD_HERE@HOST_HERE/DB_HERE') # TODO: fill the blanks
Session = sessionmaker(bind=engine)

# maps & variables
name_counts = defaultdict(int)

map_gender = {
        u'남': 'm',
        u'여': 'f',
        }

map_gender_int = {
        u'남': 1,
        u'여': 2,
        }

map_election = {
        19: '20120411',
        18: '20080409',
        17: '20040415',
        16: '20000413',
        15: '19960411',
        14: '19920324',
        13: '19880426',
        12: '19850212',
        11: '19810325',
        10: '19781212',
        9: '19730227',
        8: '19710525',
        7: '19670608',
        6: '19631126',
        5: '19600729',
        4: '19580502',
        3: '19540520',
        2: '19500530',
        1: '19480510',
        }

# functions
def preprocess(person):
    person['name_kr'] = person['name_kr'].replace(' ', '')

def migrate(session, r):
    person_id = add_person(session, r)
    add_parties(session, r)
    add_elections(session, r)
    add_candidacies(session, r, person_id)
    add_party_affiliations(session, r, person_id)
    #add_experience(session, r)
    #add_school(session, r)
    #add_education(session, r)

def add_person(session, r):
    person_id = get_person_id(r)

    if not has_person(session, person_id):
        gender = map_gender[r['sex']]
        birthday = '%04d%02d%02d' % (
                int(r.get('birthyear', 0)),
                int(r.get('birthmonth', 0)),
                int(r.get('birthday', 0))
                )

        person = Person(
                id=person_id, # FIXME: 이름 규칙
                name=r['name_kr'],
                name_cn=r['name_cn'],
                gender=gender,
                birthday=birthday,
                twitter=r.get('twitter', None),
                facebook=r.get('facebook', None),
                blog=r.get('blog', None),
                homepage=r.get('homepage', None),
                )

        # TODO: address 추가
        session.add(person)

    return person_id

def get_person_id(person):
    name = person['name_kr']
    name_counts[name] += 1
    count = name_counts[name]
    return '%04d%d%d' % (
            int(person['birthyear']),
            map_gender_int[person['sex']],
            count
            )

def has_person(session, person_id):
    return session.query(Person).filter_by(id=person_id).count() > 0

def get_person(session, person_id):
    return session.query(Person).filter_by(id=person_id).one()

def add_parties(session, r):
    add_party(session, r['party'])
    for age, candidacy in r['assembly'].items():
        add_party(session, candidacy['party'])

def add_party(session, name):
    if name and not has_party(session, name):
        party = Party(name=name)
        session.add(party)

def has_party(session, name):
    return session.query(Party).filter_by(name=name).count() > 0

def get_party(session, party_id):
    return session.query(Party).filter_by(id=party_id).one()

def add_elections(session, r):
    for age, candidacy in r['assembly'].items():
        add_election(session, age=int(age), type='assembly')

def add_election(session, age, type):
    if not has_election(session, age=age, type='assembly'):
        election = Election('assembly', age, date=map_election[age])
        session.add(election)

def has_election(session, age, type):
    return session.query(Election)\
            .filter_by(age=age, type='assembly').count() > 0

def add_candidacies(session, r, person_id):
    for age, candidacy in r['assembly'].items():
        add_candidacy(session, person_id, age, candidacy)

def add_candidacy(session, person_id, age, candidacy):
    election_id = get_election_id(session, age)
    party_id = get_party_id(session, candidacy['party'])
    region1, region2, region3 = parse_region(candidacy['district'])
    candidacy = Candidacy(
            person_id=person_id,
            election_id=election_id,
            party_id=party_id,
            region1=region1,
            region2=region2,
            region3=region3,
            is_elected=candidacy['elected'],
            cand_no=to_int(candidacy.get('cand_no', 0)),
            vote_score=to_int(candidacy.get('votenum', 0)),
            vote_share=to_float(candidacy.get('voterate', 0)),
            )
    session.add(candidacy)

def to_int(num):
    if type(num) != int and (not hasattr(num, 'isdigit') or not num.isdigit()):
        return 0
    return int(num)

def to_float(num):
    if type(num) not in [int, float]\
            and (not hasattr(num, 'isdigit') or not num.isdigit()):
        return 0
    return float(num)

def get_election_id(session, age):
    election = session.query(Election)\
            .filter_by(type='assembly', age=age).one()
    return election.id

def get_party_id(session, name):
    party = session.query(Party)\
            .filter_by(name=name).one()
    return party.id

def parse_region(region):
    t = region.split()
    region1, region2, region3 = t[0], ' '.join(t[1:]), None
    if region2 and region2[-1] in [u'갑', u'을', u'병', u'정']:
        region3 = region2[-1]
        region2 = region2[:-1]
    return (region1, region2, region3)

def add_party_affiliations(session, r, person_id):
    party_id = get_party_id(session, r['party'])
    add_party_affiliation(session, person_id, party_id)

    for age, candidacy in r['assembly'].items():
        party_id = get_party_id(session, candidacy['party'])
        add_party_affiliation(session, person_id, party_id, False)

def add_party_affiliation(session, person_id, party_id,
        is_current_member=True):

    # 같은 정당에 여러 번 들어갈 수 있음
    person = get_person(session, person_id)
    party = get_party(session, party_id)
    person.parties.append(party)

def create_db():
    Base.metadata.create_all(engine)

def migrate_all():
    with mongodb('localhost', 27017, 'popongdb') as db:
        for no in xrange(1, 20):
            print '%d대' % no
            session = Session()
            people = db['people'].find({ 'assembly_no': no })
            for person in people:
                preprocess(person)
                print person['name_kr']
                try:
                    migrate(session, person)
                except Exception, e:
                    import pprint
                    pprint.pprint(person)
                    raise e
            session.commit()
            session.close()
