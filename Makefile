init:
	git submodule init
	git submodule update
	.conf.samples/copyall.sh

extract_i18n:
	pybabel extract -F babel.cfg -k ngettext -k lazy_gettext -o pokr/messages.pot .
	pybabel update -i pokr/messages.pot -d pokr/translations

update_i18n:
	pybabel compile -d pokr/translations

create_db:
	sudo -u postgres psql -h localhost -U postgres -c 'CREATE DATABASE popongdb;'\
	&& sudo -u postgres psql -d popongdb -f pokr.dump

init_db:
	./shell.py db init
	alembic stamp head

.PHONY: install init extract_i18n update_i18n init_db
