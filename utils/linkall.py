#!/usr/bin/python
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from builtins import object
from cgi import escape
import re

from flask import url_for


__all__ = ['init_app']


year_re = '[1-9][0-9]{3}'


def init_app(app, keyword_re=''):
    keyword_re = keyword_re or year_re
    linkall = LinkAllFilter(keyword_re).get()
    app.jinja_env.filters['linkall'] = linkall


def url_keyword(keyword):
    return url_for('entity_page', keyword=keyword)


def match_to_link(m):
    keyword = m.group(0)
    return '<a href="%s">%s</a>' % (url_keyword(keyword), keyword)


class LinkAllFilter(object):

    def __init__(self, regexp):
        self.regexp = re.compile(regexp)
        self.replacer = match_to_link

    def get(self):
        def linkall(s):
            s = escape(s)
            replaced = self.regexp.sub(self.replacer, s)
            return replaced

        return linkall
