init:
	git submodule init
	git submodule update
	.conf.samples/copyall.sh

install:
	pip install git+https://github.com/teampopong/popong-models.git
	pip install git+https://github.com/teampopong/popong-data-utils.git
	cd /tmp
	git clone git@github.com:teampopong/popong-nlp.git
	cd popong-nlp
	git submodule init
	git submodule update
	python setup.py install

extract_i18n:
	pybabel extract -F babel.cfg -k ngettext -k lazy_gettext -o pokr/messages.pot .
	pybabel update -i pokr/messages.pot -d pokr/translations

update_i18n:
	pybabel compile -d pokr/translations

.PHONY: install init extract_i18n update_i18n init_db
