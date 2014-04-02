#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse

from pokr import app


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int, nargs='?', default=50029)
    parser.add_argument('-d', dest='debug', const=True, nargs='?')
    parser.add_argument('-l', dest='locale', default='auto',
                        help='force locale (e.g. en, kr)')
    return parser.parse_args()


def apply_args(app, args):
    if not args.debug is None:
        app.debug = args.debug
    if args.locale in app.LOCALES:
        app.babel.force_locale(args.locale)


# standalone mode
if __name__ == '__main__':
    args = parse_args()
    apply_args(app, args)
    app.run(host='0.0.0.0', port=args.port)

