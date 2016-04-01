#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import calendar
import datetime
from itertools import groupby

from flask import render_template

calendar.setfirstweekday(calendar.SUNDAY)

def classes_of_a_date(y, m, d):
    date = datetime.date(y, m, d)
    today = datetime.date.today()
    classlist = []

    if today == date:
        classlist.append('today')
    elif today < date:
        classlist.append('future')
    else:
        classlist.append('past')
    return classlist


def year(year, events=None):
    groups = groupby(events, lambda o: o['date'])
    events = {
        date: list(events)
        for date, events in groups
    }
    return render_template('widgets/calendar.html',
                           # functions
                           calendar=calendar,
                           date=datetime.date,
                           classes_of_a_date=classes_of_a_date,

                           # data
                           year=year,
                           events=events,
                          )
