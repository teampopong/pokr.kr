import settings
from flask import g, request
from utils.nlp.nero.romanize import name2eng as n2e, party2eng as p2e


default_locale = settings.BABEL_SETTINGS['default_locale']


def get_locale():
    locale = request.host.split('.')[0]
    if locale not in settings.LOCALES:
        locale = default_locale
    return locale


def name2eng(name):
    if get_locale() != 'ko':
        return n2e(name)
    return name


def party2eng(party):
    if get_locale() != 'ko':
        return p2e(party)
    return party
