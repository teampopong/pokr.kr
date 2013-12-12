# -*- coding: utf-8 -*-

from collections import defaultdict
import json
import os.path

from flask import abort, current_app
from sqlalchemy import func
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from controllers.base import Controller
from database import db_session
from models.candidacy import Candidacy
from models.election import current_assembly_id, Election
from models.person import Person
from models.region import Region


class RegionController(Controller):
    model = 'region'

    @classmethod
    def legislator_of(cls, region_id, assembly_id=None):
        if not region_id:
            return None
        if not assembly_id:
            assembly_id = current_assembly_id()

        region = Region.query.filter_by(id=region_id).one()
        original_region = region

        legislator = None
        while not legislator and region:
            legislators = region.candidates\
                                .filter(Candidacy.assembly_id == assembly_id)\
                                .filter_by(is_elected=True)

            try:
                legislator = legislators.one()
            except MultipleResultsFound as e:
                legislator = guess_legislator(legislators, original_region,
                                              assembly_id)
                break
            except NoResultFound as e:
                region = region.parents.order_by(False)\
                                       .order_by(func.length(Region.id).desc())\
                                       .first()

        return legislator

    @classmethod
    def officials_grouped_by_assembly_id(cls, region_id):
        officials_ = db_session.query(Person.id, Candidacy.assembly_id)\
                     .filter(Candidacy.person_id == Person.id)\
                     .filter(Candidacy.district_id.any(region_id))\
                     .filter(Candidacy.is_elected == True)\
                     .group_by(Person.id, Candidacy.election_id)

        res = defaultdict(list)
        for person_id, assembly_id in officials_:
            res[assembly_id].append(person_id)
        return res


def guess_legislator(legislators, region, assembly_id):
    for legislator in legislators:
        district = json.loads(legislator.extra_vars)\
                       .get('assembly', {})\
                       .get(str(assembly_id), {})\
                       .get('district')
        district_name = district.strip().split()[-1]
        print legislator.name, district_name, region.district_name
        if district_name == region.district_name:
            return legislator

