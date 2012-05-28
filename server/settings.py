#!/usr/bin/env python

from apps import figures

SERVER_SETTINGS = {
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
        ('/figures', figures.app)
        ]
