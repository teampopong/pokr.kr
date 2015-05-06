#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from pokr import app, bootstrap


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int, nargs='?', default=50029)
    parser.add_argument('-d', dest='debug', const=True, default=False, nargs='?')
    parser.add_argument('-l', dest='locale', default='auto',
                        help='force locale (e.g. en, kr)')
    return parser.parse_args()


def apply_args():
    args = parse_args()
    for key, val in args.__dict__.iteritems():
        setattr(app, key, val)



# standalone mode
if __name__ == '__main__':
    apply_args()
    bootstrap()
    app.run(host='0.0.0.0', port=app.port)

# wsgi mode
else:
    bootstrap()

