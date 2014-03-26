#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse

from flask import Flask


app = Flask(__name__)
try:
    app.config.from_object('conf.api')
except ImportError as e:
    import sys
    sys.stderr.write('Error: Update conf/api.py\n')
    sys.exit(1)


if not hasattr(app, '__loaded__'):
    from pokr.database import init_db
    from api import init_app
    from utils.reverse_proxy import init_app as init_reverse_proxy

    init_db(app, login=False)
    init_app(app)
    init_reverse_proxy(app)

    setattr(app, '__loaded__', True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int, nargs='?', default=50031)
    return parser.parse_args()


# standalone mode
if __name__ == '__main__':
    args = parse_args()
    app.run(host='0.0.0.0', port=args.port)

