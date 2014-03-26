# -*- coding: utf-8 -*-

from flask import abort

from .base import Controller
from pokr.database import db_session
from pokr.models.bill import Bill
from pokr.models.bill_feed import BillFeed
from pokr.models.feed import Feed
from pokr.models.keyword import Keyword
from pokr.models.person import Person


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
    def update_address(cls, user, region_id):
        user.address_id = region_id
        db_session.commit()

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

    @classmethod
    def keyword_feeds(cls, user):
        feeds = Feed.query\
                    .with_polymorphic('*')\
                    .join(BillFeed.bill)\
                    .outerjoin(Bill._keywords)\
                    .filter(Keyword.id.in_(
                                k.id for k in user.favorite_keywords))\
                    .order_by(Feed.id.desc())\
                    .distinct(Feed.id)
        return feeds

