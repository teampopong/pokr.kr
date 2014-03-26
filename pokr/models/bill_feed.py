# -*- coding: utf-8 -*-

from sqlalchemy import Column, Date, DDL, event, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from .feed import Feed, FeedType


class BillFeed(Feed):
    __tablename__ = 'bill_feed'

    id = Column(Integer, ForeignKey('feed.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    bill_id = Column(Text, ForeignKey('bill.id', onupdate='CASCADE', ondelete='CASCADE'), index=True)
    name = Column(Text)
    proposed_date = Column(Date)
    sponsor = Column(Text)

    __mapper_args__ = {
        'polymorphic_identity': FeedType.bill,
    }

    bill = relationship('Bill', uselist=False)

    def to_html(self):
        pass # TODO


insert_bill_feed = DDL('''\
CREATE OR REPLACE FUNCTION insert_bill_feed()
    RETURNS trigger as $insert_bill_feed_trigger$
    DECLARE
        feed_id int;
    BEGIN
        INSERT INTO feed ("type") VALUES (
            'B'
        ) RETURNING id INTO feed_id;

        INSERT INTO bill_feed (id, bill_id, name, proposed_date, sponsor) VALUES (
            feed_id,
            NEW.id,
            NEW.name,
            NEW.proposed_date,
            NEW.sponsor
        );

        RETURN NULL;
    END;
    $insert_bill_feed_trigger$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS insert_bill_feed_trigger ON bill CASCADE;
CREATE TRIGGER insert_bill_feed_trigger
    AFTER INSERT ON bill
    FOR EACH ROW EXECUTE PROCEDURE insert_bill_feed();
''')
event.listen(BillFeed.__table__, 'after_create', insert_bill_feed)
