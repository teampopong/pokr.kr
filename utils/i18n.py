from flask import g
from utils.nlp.nero.romanize import name2eng as n2e, party2eng as p2e

def name2eng(name):
    # FIXME: uncomment this code
    # if g.lang != 'ko':
    #     return n2e(name)
    return name


def party2eng(party):
    # FIXME: uncomment this code
    #if g.lang != 'ko':
    #    return p2e(party)
    return party
