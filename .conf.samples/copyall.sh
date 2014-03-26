#!/bin/bash

cd "$(dirname "$0")"
cp -n alembic.ini.sample ../alembic.ini
cp -n api.py.sample ../conf/api.py
cp -n frontend.py.sample ../conf/frontend.py
cp -n stopwords.py.sample ../conf/stopwords.py
cp -n storage.py.sample ../conf/storage.py
