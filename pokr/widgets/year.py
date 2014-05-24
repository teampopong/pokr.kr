#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import calendar
import datetime
from flask import render_template

calendar.setfirstweekday(calendar.SUNDAY)

def classify(date):
    classlist = []
    today = datetime.date.today()
    if today==date:
        classlist.append('today')
    if today<date:
        classlist.append('future')
    return classlist

def format_day(y, m, d, classlist=[]):
    if d==0:
        return '<td></td>'
    else:
        date = datetime.date(y, m, d)
        classlist = classify(date)
        classes = ' class="%s"' % ' '.join(classlist) if classlist else ''
        return '<td%s>%s</td>' % (classes, str(d))

def format_month(y, m):

    def format_week(week):
        weekstr = [format_day(y, m, d) for d in week]
        return "<tr>%s</tr>" % ''.join(weekstr)

    return '<div class="month-num"><h4>%d</h4><table class="month">%s</table></div>'\
            % (m, '\n'.join(format_week(week)\
                for week in calendar.monthcalendar(y, m)))

def year(y):
    calen = ''.join(format_month(y, m) for m in range(1,13))

    return render_template('widgets/calendar.html',
            calendar=calen,
            )
