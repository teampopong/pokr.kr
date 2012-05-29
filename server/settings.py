#!/usr/bin/env python

from apps import people

SERVER_SETTINGS = {
        'host': '0.0.0.0',
        'port': 50030,
        'debug': True
        }

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
        ('/people', people.app)
        ]
