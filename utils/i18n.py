from flask import g
from utils.nlp.nero.romanize import name2eng as n2e, party2eng as p2e

class LocaleError(Exception):
    pass


def name2eng(name):
    if g.lang != 'ko':
        return n2e(name)
    return name


def party2eng(party):
    if g.lang != 'ko':
        return p2e(party)
    return party
