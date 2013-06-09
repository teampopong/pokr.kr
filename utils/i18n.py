from babel import Locale
from flask import current_app as cur_app, request
from flask.ext.babel import Babel, get_locale
from functools import wraps

from utils.nlp.utils.translit import translit


__all__ = ['PopongBabel']


class PopongBabel(Babel):

    def init_app(self, app):
        super(PopongBabel, self).init_app(app)

        self.localeselector(localeselector)

        # shortcuts
        app.babel = self
        app.LOCALES = self.list_translations() + [Locale('en')]

        # jinja filters
        app.jinja_env.filters['translit'] = filter_translit
        app.jinja_env.globals.update(translit=filter_translit)

        # context processor
        app.context_processor(inject_locales)


class InvalidLocaleError(Exception):
    pass


class NotInAppContextError(Exception):
    pass


@wraps
def babel_context(f):
    def decorated(*args, **kwargs):
        if not hasattr(cur_app, 'babel') or not hasattr(cur_app, 'LOCALES'):
            raise NotInAppContextError()

        f(*args, **kwargs)
    return decorated


@babel_context
def is_valid_locale(locale):
    return locale in cur_app.LOCALES


def assert_valid_locale(locale):
    if not is_valid_locale(locale):
        raise InvalidLocaleError()


def host(locale=None):
    assert_valid_locale(locale)

    t = request.host.split('.', 1)
    if len(t) < 2 or not is_valid_locale(t[0]):
        host = request.host
    else:
        host = t[1]

    return '{locale}.{host}'.format(locale=locale, host=host)


@babel_context
def localeselector():
    locale = request.host.split('.', 1)[0]
    if not is_valid_locale(locale):
        locale = cur_app.babel.default_locale
    return locale


@babel_context
def inject_locales():
    # TODO: caching
    locale_links = {
            locale: request.url.replace(request.host, host(locale))
            for locale in cur_app.LOCALES
        }

    return dict(locale_links=locale_links,
            locale=str(get_locale()))

def filter_translit(*args, **kwargs):
    locale = str(get_locale())
    _type = kwargs.get('type')
    if len(args) == 1:
        string = args[0]
        return translit(string, 'ko', locale, _type) if locale != 'ko' else string
    elif args:
        raise Exception('filter_translit() only accepts one or zero argument')
    else:
        return lambda x: filter_translit(x, type=_type)
