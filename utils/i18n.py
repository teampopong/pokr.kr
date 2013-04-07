import settings
from flask import g, request
from utils.nlp.utils.translit import translit


default_locale = settings.BABEL_SETTINGS['default_locale']


def get_locale():
    locale = request.host.split('.')[0]
    if locale not in settings.LOCALES:
        locale = default_locale
    return locale


def name2eng(name):
    if get_locale() != 'ko':
        return translit(name, 'ko', 'en', 'name')
    return name


def party2eng(party):
    if get_locale() != 'ko':
        return translit(party, 'ko', 'en', 'party')
    return party
