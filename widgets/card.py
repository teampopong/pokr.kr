# -*- coding: utf-8 -*-

from flask import render_template

from cache import cache
from models.person import Person


@cache.memoize(24 * 60 * 60)
def card(person_or_id, detailed=False, small=False):

    if isinstance(person_or_id, Person):
        person = person_or_id
    else:
        person = Person.query.filter_by(id=person_or_id).first()

    return render_template('widgets/card.html', person=person, detailed=detailed, small=small)

