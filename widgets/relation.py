# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from flask import render_template
from flask.ext.babel import gettext
from random import shuffle

from models.candidacy import Candidacy
from models.election import Election
from models.party import Party
from models.person import Person

def relation(person_or_id, size=4):
    if isinstance(person_or_id, Person):
        person = person_or_id
    else:
        person = Person.query.filter_by(id=person_or_id).first()

    related_people = []
    #related_people.extend((gettext('in the same party'), person)\
    #        for person in people_in_the_same_party(person))
    related_people.extend((gettext('in the same constituency'), person)\
            for person in rivals(person))
    #shuffle(related_people)

    return render_template('widgets/relation.html',
            person_id=person.id,
            related_people=related_people,
            size=size)

def people_in_the_same_party(person):
    if not person:
        return []

    party = person.cur_party

    if not party:
        return []

    return party.members

def rivals(person):
    if not person:
        return []

    candidacy = Candidacy.query.filter_by(person_id=person.id)\
            .join(Election).order_by('Election.date desc').first()

    if not candidacy:
        return []

    candidacies = Candidacy.query.filter_by(election_id=candidacy.election_id,
            region1=candidacy.region1,
            region2=candidacy.region2,
            region3=candidacy.region3
            ).all()
    candidates = [candidacy.person for candidacy in candidacies]

    return candidates
