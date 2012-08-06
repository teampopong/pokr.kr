#!/bin/bash

pybabel extract -F babel.cfg -k ngettext -k lazy_gettext -o messages.pot .
pybabel update -i messages.pot -d translations
pybabel compile -d translations
