# -*- coding: utf-8 -*-

from flask.ext.login import UserMixin
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Unicode
from sqlalchemy.orm import relationship
from popong_models import Base

from .patch import PatchMixin


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    email = Column(String(200))
    name = Column(Unicode(40), index=True)
    password = Column(String(200), default='')
    username = Column(String(200))
    address_id = Column(String(16), ForeignKey('region.id', onupdate='CASCADE', ondelete='CASCADE'), index=True)

    address = relationship('Region', uselist=False)
    favorite_keywords = relationship('Keyword',
            secondary='favorite_keyword')
    favorite_people = relationship('Person',
            secondary='favorite_person')

    def is_active(self):
        return self.active


class UserPatch(PatchMixin):
    model = User

    def update_favorite_keyword(self, keyword, method):
        keyword = Keyword.query.filter_by(name=keyword).one()

        # XXX: is it safe to db.session.commit()?
        dirty = False
        if method.lower() == 'post':
            if keyword not in self.favorite_keywords:
                self.favorite_keywords.append(keyword)
                dirty = True
        elif method.lower() == 'delete':
            if keyword.id in (k.id for k in self.favorite_keywords):
                self.favorite_keywords.remove(keyword)
                dirty = True

        if dirty:
            self.session.commit()

        return dirty

    def update_favorite_person(self, person_id, method):
        person = Person.query.filter_by(id=person_id).one()

        dirty = False
        if method.lower() == 'post':
            if person not in self.favorite_people:
                self.favorite_people.append(person)
                dirty = True
        elif method.lower() == 'delete':
            if person.id in (p.id for p in self.favorite_people):
                self.favorite_people.remove(person)
                dirty = True

        if dirty:
            self.session.commit()

        return dirty

    def update_address(self, region_id):
        self.address_id = region_id
        self.session.commit()

    @classmethod
    def district_feeds(cls, legislator):
        if not legislator:
            return None

        feeds = Feed.query\
                    .with_polymorphic('*')\
                    .join(BillFeed.bill)\
                    .outerjoin(Bill.cosponsors)\
                    .filter(Person.id == legislator.id)\
                    .order_by(Feed.id.desc())\
                    .distinct(Feed.id)
        return feeds

    def keyword_feeds(self):
        feeds = Feed.query\
                    .with_polymorphic('*')\
                    .join(BillFeed.bill)\
                    .outerjoin(Bill._keywords)\
                    .filter(Keyword.id.in_(
                                k.id for k in self.favorite_keywords))\
                    .order_by(Feed.id.desc())\
                    .distinct(Feed.id)
        return feeds

