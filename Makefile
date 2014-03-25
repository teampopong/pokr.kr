install:
	pip install -r requirements.txt

init:
	git submodule init
	git submodule update
	bash -c 'for file in `find . -name "*.sample" -not -path "./.git/*"`; do cp $$file $${file/.sample/}; done'
	chmod o-rwx alembic.ini conf/*.py

extract_i18n:
	pybabel extract -F babel.cfg -k ngettext -k lazy_gettext -o messages.pot .
	pybabel update -i messages.pot -d translations

update_i18n:
	pybabel compile -d translations

init_db:
	./shell.py db init
	alembic stamp head

.PHONY: install init extract_i18n update_i18n init_db
