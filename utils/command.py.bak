# -*- coding: utf-8 -*-

class Command(object):
    __command__ = None
    __parent__ = None

    @classmethod
    def register(cls, subparsers=None):
        if hasattr(cls, 'parser'):
            return

        if cls.__parent__:
            if not hasattr(cls.__parent__, 'parser'):
                cls.__parent__.register(subparsers)

            if not hasattr(cls.__parent__, 'subparsers'):
                cls.__parent__.create_subparser()

            subparsers = cls.__parent__.subparsers

        cls.parser = subparsers.add_parser(cls.__command__)
        cls.parser.set_defaults(run=cls.run)
        cls.init_parser_options()

    @classmethod
    def create_subparser(cls):
        if hasattr(cls, 'subparsers'):
            return

        cls.subparsers = cls.parser.add_subparsers()

        # remove runner if there are subcommands
        del cls.parser._defaults['run']

    @classmethod
    def init_parser_options(cls):
        pass

    @classmethod
    def run(cls, **kwargs):
        raise NotImplementedError()

