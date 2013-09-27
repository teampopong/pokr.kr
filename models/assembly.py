# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, Integer

from data.assembly import ASSEMBLY_TERMS
from models import CascadeForeignKey
from models.organization import Organization


assembly_terms = [None]\
               + [tuple(datetime.strptime(d, '%d %b %Y').date() for d in term)
                  for term in ASSEMBLY_TERMS]


def assembly_term(session_id):
    return assembly_terms[session_id]


class Assembly(Organization):
    __tablename__ = 'assembly'

    __mapper_args__ = {
        'polymorphic_identity': 'assembly'
    }

    id = Column(Integer, CascadeForeignKey('organization.id'), primary_key=True)
    session_id = Column(Integer, nullable=False, index=True)

    @property
    def term(self):
        return assembly_term(session_id)


def current_session_id():
    current_assembly =  Assembly.query.order_by(Assembly.session_id.desc()).first()
    return getattr(current_assembly, 'session_id', None)

