# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from flask import render_template
from flask.ext.babel import gettext
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.expression import and_, cast

from models.candidacy import Candidacy
from models.election import Election
from models.person import Person


def rivals(person_or_id, age, size=4):
    if isinstance(person_or_id, Person):
        person = person_or_id
    else:
        person = Person.query.filter_by(id=person_or_id).first()

    rivals = _rivals(person, age)
    label = gettext('in the same constituency')

    return render_template('widgets/relation.html',
            person_id=person.id,
            related_people=[(label, person) for person in rivals],
            size=size)


def _rivals(person, age):
    if not person:
        return []

    my_candidacy = Candidacy.query.filter_by(person_id=person.id)\
                                  .join(Election)\
                                  .filter(Election.age == age).one()

    if not my_candidacy:
        return []

    district_ids = [id for id in my_candidacy.district_id if id]
    if not district_ids:
        return []

    district_id = district_ids[-1]

    candidacies = Candidacy.query.filter_by(election_id=my_candidacy.election_id)\
                                 .filter(and_(cast(Candidacy.district_id, ARRAY(Text))\
                                                  .contains([district_id]),
                                              Candidacy.person_id != person.id))

    rivals = [candidacy.person for candidacy in candidacies]
    return rivals
