# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from collections import Counter

from .base import Controller


TITLE_WORDS = ['제안이유', '주요내용']
SUMMARY_SIZE = 140


class BillController(Controller):
    model = 'bill'

    @classmethod
    def truncated_summary(cls, bill, size=SUMMARY_SIZE):
        # TODO: caching
        if not bill.summary:
            return ''

        lines = bill.summary.split('\n')
        first_line = lines[0]
        if any(title_word in first_line for title_word in TITLE_WORDS):
            lines.pop(0)
            while lines and not lines[0].strip():
                lines.pop(0)
        summary = '\n'.join(lines)
        ellipsis = '…' if len(summary) > SUMMARY_SIZE else ''
        return summary[:SUMMARY_SIZE] + ellipsis

