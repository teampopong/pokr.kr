from popong_models import Candidacy, Party, Person

from . import PatchMixin


class PartyPatch(PatchMixin):
    model = Party

    # FIXME: use `relationship`
    @property
    def members(self):
        return Person.query\
                     .join(Candidacy,
                           Person.id == Candidacy.person_id)\
                     .join(Party,
                           Party.id == Candidacy.party_id)\
                     .filter(Party.id == self.id)\
                     .group_by(Person.id)

