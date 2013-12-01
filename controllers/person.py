# -*- coding: utf-8 -*-

from collections import Counter

from controllers.base import Controller


class PersonController(Controller):
    model = 'person'

    @classmethod
    def keyword_counts(cls, person, limit=10):
        # TODO: batch calculation or non-blocking operation
        elected_assembly_ids = [candidacy.age for candidacy in person.candidacies]

        if not elected_assembly_ids:
            return {}

        latest_assembly_id = max(elected_assembly_ids)
        keywords = (keyword.name
                        for bill in person.bills(latest_assembly_id)
                        for keyword in bill.keywords)
        counter = Counter(keywords)

        return dict(counter.most_common(limit))
