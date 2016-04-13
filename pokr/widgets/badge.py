# -*- coding: utf-8 -*-

from flask import render_template

def badge(name, width=30):
    return render_template('widgets/badge.html', name=name, width=width)

def badges(roles, width=30):
    '''
    'official': 'full-star',
    'proportional': 'team-work',
    'committee-head': 'leadership',
    'assembly-head': 'legal',
    '''
    return render_template('widgets/badges.html', roles=roles, width=width)
