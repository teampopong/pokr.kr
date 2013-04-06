install:
	pip install -r requirements.txt
	git submodule init
	git submodule update
	cp settings.py.sample settings.py

extract_i18n:
	pybabel extract -F babel.cfg -k ngettext -k lazy_gettext -o messages.pot .
	pybabel update -i messages.pot -d translations

update_i18n:
	pybabel compile -d translations

load_db:
	pg_restore -d popongdb data/db.sql

.PHONY: install extract_i18n update_i18n load_db
