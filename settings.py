#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from apps import people, main

SCRIPT_NAME = '/'

SERVER_SETTINGS = {
        'host': '0.0.0.0',
        'port': 50030,
        'debug': True
        }

BABEL_SETTINGS = {
        'default_locale': 'ko',
        'default_timezone': 'KST',
        }

LOCALES = ['en', 'ko']

CACHE_SETTINGS = {
        'host': '127.0.0.1',
        'port': 11211
        }

DB_SETTINGS = {
        'host': 'localhost',
        'port': 27017,
        'database': 'popongdb'
        }

apps = [
        ('home', '/', main.app),
        ('people', '/people', people.app)
        ]
