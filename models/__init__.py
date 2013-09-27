# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import event

from models._utils import Table, CascadeForeignKey


__all__ = ['Table', 'CascadeForeignKey', 'init']


# register all models
def init():
    # FIXME: dynamic import
    import models.assembly
    import models.bill
    import models.bill_keyword
    import models.bill_process
    import models.bill_status
    import models.candidacy
    import models.committee
    import models.cosponsorship
    import models.education
    import models.election
    import models.keyword
    import models.named_region
    import models.organization
    import models.organization_type
    import models.party
    import models.party_affiliation
    import models.person
    import models.person_image
    import models.pledge
    import models.region
    import models.residence
    import models.school

    for model in Table.__subclasses__():
        event.listen(model, 'before_insert', update_created)
        event.listen(model, 'before_update', update_modified)


def update_created(mapper, connection, target):
    target.created_at = datetime.now()
    target.modified_at = datetime.now()
    target.modified_by = ''  # TODO


def update_modified(mapper, connection, target):
    target.modified_at = datetime.now()
    target.modified_by = ''  # TODO

