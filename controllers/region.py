# -*- coding: utf-8 -*-

from flask import abort
from sqlalchemy import func
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from controllers.base import Controller
from models.candidacy import Candidacy
from models.election import current_age, Election
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

