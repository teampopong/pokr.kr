# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from calendar import month_abbr
from flask import render_template
from flask.ext.babel import gettext

from models.person import Person
from utils.jinja import guid_factory

ASSEMBLY_TERMS = [
    (),
    ('31 May 1948', '30 May 1950'),
    ('31 May 1950', '30 May 1954'),
    ('31 May 1954', '30 May 1958'),
    ('31 May 1958', '30 May 1960'),
    ('29 Jul 1960', '16 May 1961'),
    ('17 Dec 1963', '30 Jun 1967'),
    ('1  Jul 1967', '25 Jul 1971'),
    ('26 Jul 1971', '18 Oct 1972'),
    ('12 Mar 1973', '16 Mar 1979'),
    ('17 Mar 1979', '27 Oct 1980'),
    ('11 Apr 1981', '12 May 1985'),
    ('13 May 1985', '29 May 1988'),
    ('30 May 1988', '29 May 1992'),
    ('30 May 1992', '29 May 1996'),
    ('30 May 1996', '4  Jun 2000'),
    ('5  Jun 2000', '29 May 2004'),
    ('30 May 2004', '29 May 2008'),
    ('30 May 2008', '29 May 2012'),
    ('30 May 2012', '29 May 2016'),
]

def timeline(person_or_id):
    if isinstance(person_or_id, Person):
        person = person_or_id
    else:
        person = Person.query.filter_by(id=person_or_id).first()

    events = candidacy_events(person)

    return render_template('widgets/timeline.html',
            events=events,
            guids=guid_factory(),
            )

def event(text, start, end=None):
    return [start, end or start, text]

def birthday_event(person):
    return event(gettext('birth'),
            '{0} {1} {2}'.format(
                person.birthday_day,
                month_abbr[person.birthday_month],
                person.birthday_year
                ))

def candidacy_events(person):
    events = [candidacy_event(candidacy) for candidacy in person.candidacies]
    events.append(birthday_event(person))
    return events

def candidacy_event(candidacy):
    age = int(candidacy.age)
    term = ASSEMBLY_TERMS[age]
    if candidacy.is_elected:
        e = event(gettext('won<br>%(age)dth', age=age),
                  term[0], term[1])
    else:
        e = event(gettext('lost<br>%(age)dth', age=age),
                  term[0])
    return e
