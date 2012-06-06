#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from apps import people, main

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
        ('home', '홈', '', main.app),
        ('people', '정치인명사전', '/people', people.app)
        ]
