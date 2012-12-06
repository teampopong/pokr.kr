#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from utils.mongo_to_sqlalchemy import create_db, migrate_all

#create_db()
migrate_all()
