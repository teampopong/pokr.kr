from collections import Counter, defaultdict, OrderedDict

from popong_models import Bill, Candidacy, Party, Person, Pledge
from popong_models.cosponsorship import cosponsorship

from .patch import PatchMixin


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

    def allies(self, assembly_id=None, threshold=0.5):
        bills = self.bills_of(assembly_id)
        sponsored_bills = (bill for bill in bills if self.id in (p.id for p in bill.representative_people))
        counter = Counter()
        num_sponsored_bills = 0
        for bill in bills:
            followers = self.session\
                            .query(Person.id)\
                            .join(cosponsorship)\
                            .filter(cosponsorship.c.bill_id == bill.id)
            counter = counter + Counter(follower.id for follower in followers if follower.id != self.id)
            num_sponsored_bills += 1

        return OrderedDict(
            (key, (value + .0) / num_sponsored_bills)
                for key, value in counter.most_common(10)\
                if (value + .0) / num_sponsored_bills > threshold
        )

    def bills_of(self, assembly_id=None):
        query = Bill.query.join(cosponsorship,
                                Bill.id == cosponsorship.c.bill_id)\
                          .join(Person,
                                Person.id == cosponsorship.c.person_id)\
                          .filter_by(id=self.id)\
                          .order_by(Bill.proposed_date.desc())
        if assembly_id:
            query = query.filter(Bill.assembly_id == assembly_id)

        return query

    def keyword_counts(self, limit=10):
        # TODO: batch calculation or non-blocking operation
        elected_assembly_ids = [candidacy.assembly_id
                                for candidacy in self.candidacies
                                if candidacy.is_elected]

        if not elected_assembly_ids:
            return {}

        latest_assembly_id = max(elected_assembly_ids)
        keywords = (keyword.name
                        for bill in self.bills_of(latest_assembly_id)
                        for keyword in bill.keywords)
        counter = Counter(keywords)

        return dict(counter.most_common(limit))

    def party_history(self):
        parties_and_assembly_ids = self.parties.add_columns(Candidacy.assembly_id)
        result = []
        prev_party_id = None
        for party, assembly_id in parties_and_assembly_ids:
            if prev_party_id == party.id:
                result[-1][0].append(assembly_id)
            else:
                result.append(([assembly_id], party))
                prev_party_id = party.id
        return [(party, min(assembly_ids), max(assembly_ids)) for assembly_ids, party in result]

    def pledges_grouped_by_assembly_id(self):
        query = Pledge.query.join(Candidacy,
                                  Candidacy.id == Pledge.candidacy_id)\
                            .join(Person,
                                  Person.id == Candidacy.person_id)\
                            .filter(Person.id == self.id)\
                            .order_by(Pledge.id)

        result = defaultdict(list)
        for pledge in query:
            result[pledge.candidacy.assembly_id].append(pledge)

        return result

