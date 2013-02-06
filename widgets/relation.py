# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from flask import render_template

from models.person import Person
from models.party import Party

def relation(person_id):
    person = Person.query.filter_by(id=person_id).first()
    related_people = people_in_the_same_party(person)

    return render_template('widgets/relation.html',
            person_id=person_id,
            related_people=related_people)

def people_in_the_same_party(person):
    if not person:
        return []

    party = person.cur_party

    if not party:
        return []

    return party.members
