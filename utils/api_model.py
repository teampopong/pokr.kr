# -*- coding: utf-8 -*-

class ApiModel(object):
    '''An mixin with utility functions to make models suitable for API resources.
    Subclasses of this class should set :attr:`__kind_single__`,
    :attr:`__kind_list__` which specify the resource type.

        class Person(Base, ApiModel):
            __tablename__ = 'person'
            __kind_single__ = 'person'
            __kind_list__ = 'people'

    The subclass may override any methods of this class to extend/filter
    data given in the APIs:

        def _to_dict_light(self):
            d = self._columns_to_dict()
            extra_vars = json.loads(self.extra_vars)

            del d['extra_vars']
            d['address'] = extra_vars.get('address')
            return d
    '''
    __kind_top__ = 'gov'
    __kind_single__ = None
    __kind_list__ = None

    def to_dict(self, projection=None):
        if not hasattr(self, '__table__'):
            raise Exception('ApiModel should inherit `Base` class')

        projection = projection or 'light'
        if projection == 'light':
            return self._to_dict_light()
        elif projection == 'full':
            return self._to_dict_full()
        else:
            raise Exception('Unknown argument')

    @classmethod
    def kind(cls, _type):
        if _type == 'single':
            return '%s#%s' % (cls.__kind_top__, cls.__kind_single__)
        elif _type == 'list':
            return '%s#%s' % (cls.__kind_top__, cls.__kind_list__)
        else:
            raise Exception('Unknown argument')

    def _to_dict_light(self):
        return self._columns_to_dict()

    def _to_dict_full(self):
        return self._to_dict_light()

    def _columns_to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)

        return d

