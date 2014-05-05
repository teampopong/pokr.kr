# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from itertools import izip

from flask import render_template
from flask.ext.babel import gettext
from popong_models.candidacy import Candidacy
from popong_models.election import Election
from popong_models.person import Person
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.expression import and_, cast, desc


def rivals(person_or_id, election_id, size=4):
    if isinstance(person_or_id, Person):
        person = person_or_id
    else:
        person = Person.query.filter_by(id=person_or_id).first()

    rivals = _rivals(person, election_id)
    label = gettext('in the same constituency')

    return render_template('widgets/relation.html',
            person_id=person.id,
            related_people=[(label, person) for person in rivals],
            size=size)


def _rivals(person, election_id):
    if not person:
        return []

    my_candidacy = Candidacy.query.filter_by(person_id=person.id)\
                                  .filter_by(election_id=election_id).one()

    if not my_candidacy:
        return []

    if not my_candidacy.district or my_candidacy.district[0] == u'비례대표':
        return []

    candidacies = Candidacy.query.filter_by(election_id=my_candidacy.election_id)\
                                 .filter(and_(cast(Candidacy.district, ARRAY(Text))\
                                                  == my_candidacy.district,
                                              Candidacy.person_id != person.id))\
                                 .order_by(desc(Candidacy.vote_score)).all()

    rivals = [candidacy.person for candidacy in candidacies]
    for rival, candidacy in izip(rivals, candidacies):
        rival.u_candidacy = candidacy
    return rivals
