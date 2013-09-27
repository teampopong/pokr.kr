# -*- coding: utf-8 -*-

from flask import url_for
from sqlalchemy import Column, DateTime, event, ForeignKey, Text


class Table(object):
    created_at = Column(DateTime, index=True)
    modified_at = Column(DateTime, index=True)
    modified_by = Column(Text)

    @property
    def url(self):
        if not hasattr(self, '__endpoint__'):
            raise NotImplementedError()
        return url_for(self.__endpoint__, id=self.id)


def CascadeForeignKey(column, *args, **kwargs):
    return ForeignKey(column, *args, onupdate='CASCADE', ondelete='CASCADE', **kwargs)

