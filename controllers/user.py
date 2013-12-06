# -*- coding: utf-8 -*-

from flask import abort

from controllers.base import Controller
from database import db_session
from models.bill import Bill
from models.bill_feed import BillFeed
from models.feed import Feed
from models.keyword import Keyword
from models.person import Person


class UserController(Controller):
    model = 'user'

    @classmethod
    def update_favorite_keyword(cls, user, keyword, method):
        keyword = Keyword.query.filter_by(name=keyword).one()

        # XXX: is it safe to db_session.commit()?
        dirty = False
        if method.lower() == 'post':
            if keyword not in user.favorite_keywords:
                user.favorite_keywords.append(keyword)
                dirty = True
        elif method.lower() == 'delete':
            if keyword.id in (k.id for k in user.favorite_keywords):
                user.favorite_keywords.remove(keyword)
                dirty = True

        if dirty:
            db_session.commit()

        return dirty

    @classmethod
    def update_favorite_person(cls, user, person_id, method):
        person = Person.query.filter_by(id=person_id).one()

        dirty = False
        if method.lower() == 'post':
            if person not in user.favorite_people:
                user.favorite_people.append(person)
                dirty = True
        elif method.lower() == 'delete':
            if person.id in (p.id for p in user.favorite_people):
                user.favorite_people.remove(person)
                dirty = True

        if dirty:
            db_session.commit()

        return dirty

    @classmethod
    def keyword_feeds(cls, user):
        feeds = Feed.query\
                    .with_polymorphic('*')\
                    .join(BillFeed.bill)\
                    .outerjoin(Bill._keywords)\
                    .filter(Keyword.id.in_(
                                k.id for k in user.favorite_keywords))\
                    .order_by(Feed.id.desc())
        return feeds

