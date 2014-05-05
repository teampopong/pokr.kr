from collections import defaultdict

from flask import url_for
from sqlalchemy import func
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from popong_models import Candidacy, Election, Person, Region
from popong_models.election import current_assembly_id

from .patch import PatchMixin


class RegionPatch(PatchMixin):
    model = Region

    @property
    def url(self):
        return url_for('region', region_id=self.id)

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

    def officials_grouped_by_assembly_id(self):
        officials_ = self.session\
                         .query(Person.id, Candidacy.assembly_id)\
                         .filter(Candidacy.person_id == Person.id)\
                         .filter(Candidacy.district_id.any(self.id))\
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
        if district_name == region.district_name:
            return legislator

