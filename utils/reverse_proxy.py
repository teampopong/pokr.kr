# -*- coding: utf-8 -*-

from builtins import object
def init_app(app):
    script_name = app.config.get('SCRIPT_NAME')
    app.wsgi_app = ReverseProxied(app.wsgi_app, script_name)


class ReverseProxied(object):
    def __init__(self, app, script_name):
        self.app = app
        self.script_name = script_name

    def __call__(self, environ, start_response):
        script_name = self.script_name
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

