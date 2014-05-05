# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os

from popong_models import Bill, Candidacy, Election, Party, Person
from popong_models.cosponsorship import cosponsorship

from .patch import PatchMixin
from settings import BILLPDF_DIR, BILLTXT_DIR, STOPWORDS


TITLE_WORDS = ['제안이유', '주요내용']
DEFAULT_SUMMARY_SIZE = 200


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
                                     Person.id.distinct().count())\
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

    def truncated_summary(self, size=DEFAULT_SUMMARY_SIZE):
        # TODO: caching
        if not self.summary:
            return ''

        lines = self.summary.split('\n')
        first_line = lines[0]
        if any(title_word in first_line for title_word in TITLE_WORDS):
            lines.pop(0)
            while lines and not lines[0].strip():
                lines.pop(0)
        summary = '\n'.join(lines)
        ellipsis = '…' if len(summary) > size else ''
        return summary[:size] + ellipsis


def assembly_id_by_bill_id(bill_id):
    return int(bill_id.lstrip('Z')[:2])

