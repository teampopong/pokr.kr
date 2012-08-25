install:
	npm install -g less
	pip install -r requirements.txt

update_i18n:
	pybabel extract -F babel.cfg -k ngettext -k lazy_gettext -o messages.pot .
	pybabel update -i messages.pot -d translations
	pybabel compile -d translations

load_db:
	mongorestore -d popongdb -c people tests/data/popongdb/people

.PHONY: install update_i18n load_db
