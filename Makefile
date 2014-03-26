install:
	pip install -r requirements.txt

init:
	git submodule init
	git submodule update
	.conf.samples/copyall.sh
	cd utils/nlp
	git submodule init
	git submodule update

extract_i18n:
	pybabel extract -F babel.cfg -k ngettext -k lazy_gettext -o pokr/messages.pot .
	pybabel update -i pokr/messages.pot -d pokr/translations

update_i18n:
	pybabel compile -d pokr/translations

init_db:
	./shell.py db init
	alembic stamp head

.PHONY: install init extract_i18n update_i18n init_db
