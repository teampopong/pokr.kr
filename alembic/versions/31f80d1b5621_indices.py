"""indices

Revision ID: 31f80d1b5621
Revises: 2351e1d04612
Create Date: 2014-05-21 22:22:02.525834

"""

# revision identifiers, used by Alembic.
revision = '31f80d1b5621'
down_revision = '2351e1d04612'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index(op.f('ix_bill_assembly_id'), 'bill', ['assembly_id'], unique=False)
    op.create_index(op.f('ix_bill_decision_date'), 'bill', ['decision_date'], unique=False)
    op.create_index(op.f('ix_bill_is_processed'), 'bill', ['is_processed'], unique=False)
    op.create_index(op.f('ix_bill_link_id'), 'bill', ['link_id'], unique=False)
    op.create_index(op.f('ix_bill_proposed_date'), 'bill', ['proposed_date'], unique=False)
    op.create_index(op.f('ix_bill_sponsor'), 'bill', ['sponsor'], unique=False)
    op.create_index(op.f('ix_bill_feed_bill_id'), 'bill_feed', ['bill_id'], unique=False)
    op.create_index(op.f('ix_bill_review_end_date'), 'bill_review', ['end_date'], unique=False)
    op.create_index(op.f('ix_bill_review_name'), 'bill_review', ['name'], unique=False)
    op.create_index(op.f('ix_bill_review_start_date'), 'bill_review', ['start_date'], unique=False)
    op.create_index(op.f('ix_bill_status_name'), 'bill_status', ['name'], unique=False)
    op.create_index(op.f('ix_cosponsorship_is_sponsor'), 'cosponsorship', ['is_sponsor'], unique=False)
    op.create_index(op.f('ix_election_assembly_id'), 'election', ['assembly_id'], unique=False)
    op.create_index(op.f('ix_election_is_regular'), 'election', ['is_regular'], unique=False)
    op.create_index(op.f('ix_feed_created_at'), 'feed', ['created_at'], unique=False)
    op.create_index(op.f('ix_query_log_query'), 'query_log', ['query'], unique=False)
    op.create_index(op.f('ix_query_log_timestamp'), 'query_log', ['timestamp'], unique=False)
    op.create_index(op.f('ix_region_district_name'), 'region', ['district_name'], unique=False)
    op.create_index(op.f('ix_user_address_id'), 'user', ['address_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_user_address_id'), table_name='user')
    op.drop_index(op.f('ix_region_district_name'), table_name='region')
    op.drop_index(op.f('ix_query_log_timestamp'), table_name='query_log')
    op.drop_index(op.f('ix_query_log_query'), table_name='query_log')
    op.drop_index(op.f('ix_feed_created_at'), table_name='feed')
    op.drop_index(op.f('ix_election_is_regular'), table_name='election')
    op.drop_index(op.f('ix_election_assembly_id'), table_name='election')
    op.drop_index(op.f('ix_cosponsorship_is_sponsor'), table_name='cosponsorship')
    op.drop_index(op.f('ix_bill_status_name'), table_name='bill_status')
    op.drop_index(op.f('ix_bill_review_start_date'), table_name='bill_review')
    op.drop_index(op.f('ix_bill_review_name'), table_name='bill_review')
    op.drop_index(op.f('ix_bill_review_end_date'), table_name='bill_review')
    op.drop_index(op.f('ix_bill_feed_bill_id'), table_name='bill_feed')
    op.drop_index(op.f('ix_bill_sponsor'), table_name='bill')
    op.drop_index(op.f('ix_bill_proposed_date'), table_name='bill')
    op.drop_index(op.f('ix_bill_link_id'), table_name='bill')
    op.drop_index(op.f('ix_bill_is_processed'), table_name='bill')
    op.drop_index(op.f('ix_bill_decision_date'), table_name='bill')
    op.drop_index(op.f('ix_bill_assembly_id'), table_name='bill')

