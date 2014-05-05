# -*- coding: utf-8 -*-

from flask import render_template

from popong_models.person import Person


def card(person_or_id, **kwargs):

    if isinstance(person_or_id, Person):
        person = person_or_id
    else:
        person = Person.query.filter_by(id=person_or_id).first()

    return render_template('widgets/card.html', person=person, **kwargs)

