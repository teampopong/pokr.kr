install:
	pip install -r requirements.txt
	git submodule init
	git submodule update
	cp alembic.ini.sample alembic.ini
	for f in conf/*.sample; do cp "$f" "conf/`basename $f .sample`"; done
	chmod o-rwx alembic.ini conf/*.py

extract_i18n:
	pybabel extract -F babel.cfg -k ngettext -k lazy_gettext -o messages.pot .
	pybabel update -i messages.pot -d translations

update_i18n:
	pybabel compile -d translations

init_db
	./shell db init
	alembic stamp head

.PHONY: install extract_i18n update_i18n init_db
