import os

from popong_models import Bill, Candidacy, cosponsorship, Election, Party, Person

from . import PatchMixin
from settings import BILLPDF_DIR, BILLTXT_DIR, STOPWORDS


class BillPatch(PatchMixin):
    model = Bill

    @property
    def keywords(self):
        return [keyword for keyword in self._keywords
                if keyword.name not in STOPWORDS]

    @property
    def document_pdf_path(self):
        assembly_id = assembly_id_by_bill_id(self.id)
        filepath = '%s/%d/%s.pdf' % (BILLPDF_DIR, assembly_id, self.id)
        if os.path.exists(filepath):
            return filepath
        else:
            return None

    @property
    def document_text_path(self):
        assembly_id = assembly_id_by_bill_id(self.id)
        filepath = '%s/%d/%s.txt' % (BILLTXT_DIR, assembly_id, self.id)
        if os.path.exists(filepath):
            return filepath
        else:
            return None

    @property
    def party_counts(self):
        # TODO: cache (denormalize)
        party_counts = self.session\
                           .query(Party.name,
                                     func.count(distinct(Person.id)))\
                           .join(Candidacy)\
                           .join(Election)\
                           .filter(Election.assembly_id == self.assembly_id)\
                           .join(Person)\
                           .join(cosponsorship)\
                           .join(Bill)\
                           .filter(Bill.id == self.id)\
                           .group_by(Party.id)
        return [(party, int(count)) for party, count in party_counts]

    @property
    def representative_people(self):
        return [cosponsor
                for cosponsor in self.cosponsors
                if cosponsor.name in self.sponsor]


def assembly_id_by_bill_id(bill_id):
    return int(bill_id.lstrip('Z')[:2])

