#!/usr/bin/env python

from flask import Flask, jsonify
import memcache
from pymongo import Connection
import settings
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException


##### utils #####

def create_server(name, **kwargs):
    '''
    Create Flask server with database and cache server connection.
    '''

    def database(host, port, database):
        connection = Connection(host, port)
        db = connection[database]
        return db

    server = Flask(name, **kwargs)
    server.db = database(**settings.db)
    server.cache = memcache.Client(['%(host)s:%(port)d' % settings.cache])

    return server


def ensure_error_in_json(server):
    '''
    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    '''

    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    for code in default_exceptions.iterkeys():
        server.error_handler_spec[None][code] = make_json_error


def register_apps(server):
    '''
    Register all app modules specified in settings.
    '''

    for url_prefix, app in settings.apps:
        server.register_blueprint(app, url_prefix=url_prefix)


def main():
    server = create_server(__name__)

    ensure_error_in_json(server)
    register_apps(server)

    server.run(**settings.server)


##### main #####

if __name__ == '__main__':
    main()
