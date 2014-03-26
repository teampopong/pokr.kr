# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
from glob import glob
from itertools import izip
from os.path import basename
import sys

from pokr.database import transaction
from pokr.models.bill import Bill
from pokr.models.bill_keyword import bill_keyword
from pokr.models.keyword import Keyword
from utils.command import Command
from utils.nlp.extractor.extract import keywords as extract_keywords


class BillKeywordCommand(Command):
    __command__ = 'bill_keyword'


class UpdateBillKeywordsCommand(Command):
    __command__ = 'update'
    __parent__ = BillKeywordCommand

    @classmethod
    def init_parser_options(cls):
        cls.parser.add_argument('files')

    @classmethod
    def run(cls, files, **kwargs):
        insert_bill_keywords(files)


def insert_bill_keywords(files):
    with transaction() as session:
        existing_bill_ids = [bill.id for bill in Bill.query]
        keyword_store = KeywordStore(session)
        for file_ in glob(files):
            filename = basename(file_)
            print 'processing %s' % filename
            sys.stdout.flush()
            bill_id = filename.split('.', 1)[0]
            if bill_id not in existing_bill_ids:
                continue
            with open(file_, 'r') as f:
                keywords = extract_keywords(f)
            keyword_ids = [keyword_store.id(keyword[0]) for keyword in keywords]
            keyword_store.sync()
            existing_keywords_for_bill = set(bk.keyword_id
                    for bk in session.query(bill_keyword)\
                                     .filter(bill_keyword.c.bill_id == bill_id)
            )

            new_bill_keywords = [
                {
                    'bill_id': bill_id,
                    'keyword_id': keyword_id,
                    'weight': weight,
                }
                for (_, weight), keyword_id in izip(keywords, keyword_ids)
                if keyword_id not in existing_keywords_for_bill
            ]

            if new_bill_keywords:
                session.execute(bill_keyword.insert(), new_bill_keywords)


class KeywordStore(object):
    dict_ = {}
    last_id = 0
    last_id_in_db = 0

    def __init__(self, session=None):
        if session:
            self.init(session)

    def init(self, session):
        bss = session.query(Keyword).order_by(Keyword.id).all()
        self.dict_ = {
            keyword.name: keyword.id
            for keyword in bss
        }
        self.last_id_in_db = self.last_id = bss[-1].id if bss else 0
        self.session = session

    def id(self, name):
        if name not in self.dict_:
            self.last_id += 1
            self.dict_[name] = self.last_id
        return self.dict_[name]

    def sync(self):
        keywords = [{
                        'id': id,
                        'name': name
                    } for name, id in self.dict_.items()
                      if id > self.last_id_in_db]
        if keywords:
            self.session.execute(Keyword.__table__.insert(), keywords)
            self.session.flush()
        self.last_id_in_db = self.last_id
