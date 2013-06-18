# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from glob import glob
from os.path import basename

from database import transaction
from models.bill_keyword import bill_keyword
from models.keyword import Keyword
from utils.nlp.extractor.extract import keywords as extract_keywords

def insert_bill_keywords(files):
    existing_keywords = {
            keyword.name: keyword.id
            for keyword in Keyword.query
        }

    with transaction() as session:
        for file_ in glob(files):
            bill_id = basename(file_).split('.', 1)[0]
            with open(file_, 'r') as f:
                keywords = extract_keywords(f)
            new_keywords = [keyword[0]
                                for keyword in keywords
                                if keyword[0] not in existing_keywords]
            session.add_all(Keyword(keyword) for keyword in new_keywords)
            session.flush()
            # FIXME: improve
            existing_keywords = {
                    keyword.name: keyword.id
                    for keyword in session.query(Keyword)
                }

            session.execute(bill_keyword.insert(), [
                {
                    'bill_id': bill_id,
                    'keyword_id': existing_keywords[keyword],
                    'weight': weight,
                }
                for keyword, weight in keywords
            ])

