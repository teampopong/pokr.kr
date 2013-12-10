# -*- coding: utf-8 -*-

from collections import defaultdict

from flask import abort
from sqlalchemy import func
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from controllers.base import Controller
from database import db_session
from models.candidacy import Candidacy
from models.election import current_age, Election
from models.person import Person
from models.region import Region


class RegionController(Controller):
    model = 'region'

    @classmethod
    def legislator_of(cls, region_id):
        if not region_id:
            return None

        age = current_age()
        region = Region.query.filter_by(id=region_id).one()

        legislator = None
        while not legislator and region:
            try:
                legislator = region.candidates.filter(Candidacy.age == age)\
                                              .filter_by(is_elected=True)\
                                              .one()
            except MultipleResultsFound as e:
                break
            except NoResultFound as e:
                region = region.parents.order_by(False)\
                                       .order_by(func.length(Region.id).desc())\
                                       .first()

        return legislator

    @classmethod
    def officials_grouped_by_age(cls, region_id):
        officials_ = db_session.query(Person.id, Candidacy.age)\
                     .filter(Candidacy.person_id == Person.id)\
                     .filter(Candidacy.district_id.any(region_id))\
                     .filter(Candidacy.is_elected == True)\
                     .group_by(Person.id, Candidacy.election_id)

        res = defaultdict(list)
        for person_id, age in officials_:
            res[age].append(person_id)
        return res

