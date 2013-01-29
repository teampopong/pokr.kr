# -*- encoding: utf-8 -*-

import settings

default_locale = settings.BABEL_SETTINGS['default_locale']

def host(locale=default_locale):
    if locale not in settings.LOCALES:
        locale = default_locale
    return '%s.popong.com' % locale
