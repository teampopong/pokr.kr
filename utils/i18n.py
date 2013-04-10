from flask import request
from flask.ext.babel import Babel
from flask.ext.babel import refresh as babel_refresh

from utils.nlp.utils.translit import translit


__all__ = ['babel', 'init_app']


babel = Babel()


class InvalidLocaleError(Exception):
    pass


def init_app(app, **settings):
    babel.init_app(app)

    # babel settings
    for key, val in settings.items():
        app.config[('babel_%s' % key).upper()] = val
    babel.localeselector(get_locale)
    babel_refresh()

    # helper
    babel.LOCALES = babel.list_translations() + ['en']

    # jinja filters
    app.jinja_env.filters['name2eng'] = name2eng
    app.jinja_env.filters['party2eng'] = party2eng

    # context processor
    @app.context_processor
    def inject_locales():
        locale_links = {
                locale: request.url.replace(request.host, host(locale))
                for locale in babel.LOCALES
            }
        return dict(locale_links=locale_links,
                locale=get_locale())


def host(locale=None):
    if locale not in babel.LOCALES:
        raise InvalidLocaleError()

    if request.host.split('.', 1)[0] not in babel.LOCALES:
        host = request.host
    else:
        host = request.host.split('.', 1)[1]

    return '{locale}.{host}'.format(locale=locale, host=host)


def get_locale():
    locale = request.host.split('.', 1)[0]
    if locale not in babel.LOCALES:
        locale = babel.default_locale
    return locale


def name2eng(name):
    if get_locale() != 'ko':
        return translit(name, 'ko', 'en', 'name')
    return name


def party2eng(party):
    if get_locale() != 'ko':
        return translit(party, 'ko', 'en', 'party')
    return party
