#!/bin/bash

cd "$(dirname "$0")"
cp -n alembic.ini.sample ../alembic.ini
cp -n api_settings.py.sample ../api_settings.py
cp -n settings.py.sample ../settings.py
