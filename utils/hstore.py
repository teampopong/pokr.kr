""":mod:`hstore` --- Using PostgreSQL hstore with SQLAlchemy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   I released it under Public Domain.  Feel free to use!

It provides :class:`Hstore` type which makes you to store Python
dictionaries into hstore columns in PostgreSQL.  For example::

    from sqlalchemy import Column
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.types import Integer, Unicode
    from hstore import Hstore


    Base = declarative_base()


    class Person(Base):
        '''Person model class that can store extra data as well.'''

        id = Column(Integer, primary_key=True)
        name = Column(Unicode, nullable=False)
        extra_data = Column(Hstore, nullable=False, default={})
        __tablename__ = 'people'

and then you can use it like:

>>> p = Person(name=u'Hong Minhee',
...            extra_data={'twitter': 'hongminhee', 'github': 'dahlia'})
>>> session.add(p)
>>> session.flush()

It will be stored in PostgreSQL using hstore::

    # SELECT * FROM people;
     id | name        | extra_data
    ----+-------------+--------------------------------------------
     1  | Hong Minhee | "twitter"=>"hongminhee", "github"=>"dahlia"
    (1 row)

"""
import collections
import sqlalchemy.types
from sqlalchemy.ext.mutable import MutableDict


__license__ = 'Public Domain'


class Hstore(sqlalchemy.types.UserDefinedType):
    """The ``hstore`` type that stores a dictionary.  It can take an any
    instance of :class:`collections.Mapping`.

    It can be extended to store other types than string e.g.::

        class IntegerBooleanHstore(Hstore):
            '''The ``hstore`` type for integer keys and boolean values.'''

            def map_bind_key(self, key):
                if key is not None:
                    return unicode(key)

            def map_bind_value(self, value):
                if value is not None:
                    return u't' if value else u'f'

            def map_result_key(self, key):
                if key is not None:
                    return int(key)

            def map_result_value(self, value):
                if value is not None:
                    return value == u't'

    :param value_nullable: to prevent ``None`` (``NULL``) for dictionary
                           values, set it ``True``. default is ``False``
    :type value_nullable: :class:`bool`

    """

    def __init__(self, value_nullable=True):
        self.value_nullable = bool(value_nullable)

    def map_bind_key(self, key):
        """The mapping function that is used for binding keys.  The default
        implementation is just a string identity function.

        :param key: a key object to bind
        :returns: a mapped key string
        :rtype: :class:`unicode`

        """
        if key is None:
            return
        if not isinstance(key, basestring):
            raise TypeError('hstore key must be a string, not ' + repr(key))
        return unicode(key)

    def map_bind_value(self, value):
        """The mapping function that is used for binding values.
        The default implementation is just a string identity function.

        :param value: a value to bind
        :returns: a mapped value string
        :rtype: :class:`unicode`

        """
        if value is None:
            return
        if not isinstance(value, basestring):
            raise TypeError('hstore value must be a string, not ' +
                            repr(value))
        return unicode(value)

    def map_result_key(self, key):
        """The mapping function that is used for resulting keys.  The default
        implementation is just an identity function.

        :param key: a raw key of the result
        :type key: :class:`unicode`
        :returns: a mapped key object

        """
        return key

    def map_result_value(self, value):
        """The mapping function that is used for resulting values.
        The default implementation is just an identity function.

        :param key: a raw value of the result
        :type key: :class:`unicode`
        :returns: a mapped value

        """
        return value

    def get_col_spec(self):
        return 'hstore'

    def is_mutable(self):
        return True

    def compare_values(self, x, y):
        x = None if x is None else dict(x)
        y = None if y is None else dict(y)
        return x == y

    def copy_value(self, value):
        if value is not None:
            return dict(value)

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return
            if not isinstance(value, collections.Mapping):
                raise TypeError('expected a collections.Mapping object, not '
                                + repr(value))
            items = getattr(value, 'iteritems', value.items)()
            map_bind_key = self.map_bind_key
            def map_key(key):
                if key is None:
                    raise TypeError('hstore key cannot be None')
                return map_bind_key(key)
            if self.value_nullable:
                map_value = self.map_bind_value
            else:
                map_bind_value = self.map_bind_value
                def map_value(value):
                    if value is None:
                        raise TypeError('hstore value cannot be None')
                    return map_bind_value(value)
            return dict((map_key(k), map_value(v)) for k, v in items)
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            map_key = self.map_result_key
            map_value = self.map_result_value
            return dict((map_key(k), map_value(v))
                        for k, v in value.iteritems())
        return process


MutableDict.associate_with(Hstore)

