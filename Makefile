install:
	pip install -r requirements.txt
	git submodule init
	git submodule update
	cp alembic.ini.sample alembic.ini
	cp conf/frontend.py.sample conf/frontend.py
	cp conf/regions.py.sample conf/regions.py
	cp conf/storage.py.sample conf/storage.py

extract_i18n:
	pybabel extract -F babel.cfg -k ngettext -k lazy_gettext -o messages.pot .
	pybabel update -i messages.pot -d translations

update_i18n:
	pybabel compile -d translations

load_db:
	pg_restore -d popongdb data/schema.sql

.PHONY: install extract_i18n update_i18n load_db
