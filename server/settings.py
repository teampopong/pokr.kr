#!/usr/bin/env python

from apps import figures

server = {
        'port': 50030,
        'debug': True
        }

cache = {
        'host': '127.0.0.1',
        'port': 11211
        }

db = {
        'host': 'localhost',
        'port': 27017,
        'database': 'popong'
        }

apps = [
        ('/figures', figures.app)
        ]
