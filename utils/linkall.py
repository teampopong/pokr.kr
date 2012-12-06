#!/usr/bin/python
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from cgi import escape
import re

def match_to_link(url_map, m):
    keyword = m.group(0)
    return '<a href="%s">%s</a>' % (url_map(keyword), keyword)

class LinkAllFilter(object):

    def __init__(self, url_map, regexp):
        self.regexp = re.compile(regexp)
        self.replacer = lambda m: match_to_link(url_map, m)

    def get(self):
        def linkall(s):
            s = escape(s)
            replaced = self.regexp.sub(self.replacer, s)
            return replaced

        return linkall
