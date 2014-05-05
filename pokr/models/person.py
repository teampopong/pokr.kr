from popong_models import Candidacy, Party, Person

from . import PatchMixin


class PersonPatch(PatchMixin):
    model = Person

    # FIXME: replace this with `relationship`
    @property
    def parties(self):
        parties = Party.query.join(Candidacy,
                                   Candidacy.party_id == Party.id)\
                            .join(Person,
                                  Person.id == Candidacy.person_id)\
                            .filter(Person.id == self.id)\
                            .order_by(Candidacy.assembly_id.desc())
        return parties

    @property
    def cur_party(self):
        return self.parties.first()

