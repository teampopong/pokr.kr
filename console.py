#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from utils.mongo_to_sqlalchemy import create_db, migrate_all

def main(command):
    if command == 'create':
        create_db()
    elif command == 'migrate':
        migrate_all()

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
