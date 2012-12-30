#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import current_app, url_for

def asset(relpath):
    if current_app.debug:
        return url_for('static', filename=relpath)
    else:
        return '//popong.com/static/%s' % relpath
