# -*- coding: utf-8 -*-

from collections import Counter

from controllers.base import Controller


class PersonController(Controller):
    model = 'person'
    STOPWORDS = []

    @classmethod
    def init(cls, app):
        with app.open_resource('data/stopwords.txt') as f:
            tokens = f.readlines()
        cls.STOPWORDS = [token.strip().decode('utf-8')
                            for token in tokens]

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
        keywords = (keyword for keyword in keywords
                            if keyword not in cls.STOPWORDS)
        counter = Counter(keywords)

        return dict(counter.most_common(limit))
