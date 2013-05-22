"""cascading delete constraint on bill tables

Revision ID: 17b5e9dda9a0
Revises: 3d2e69b77518
Create Date: 2013-05-22 12:08:23.074692

"""

# revision identifiers, used by Alembic.
revision = '17b5e9dda9a0'
down_revision = '3d2e69b77518'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint("bill_review_bill_id_fkey", 'bill_review')
    op.create_foreign_key("bill_review_bill_id_fkey", 'bill_review', 'bill', ['bill_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint("bill_withdrawal_bill_id_fkey", 'bill_withdrawal')
    op.create_foreign_key("bill_withdrawal_bill_id_fkey", 'bill_withdrawal', 'bill', ['bill_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint("cosponsorship_bill_id_fkey", 'cosponsorship')
    op.create_foreign_key("cosponsorship_bill_id_fkey", 'cosponsorship', 'bill', ['bill_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')


def downgrade():
    op.drop_constraint("bill_review_bill_id_fkey", 'bill_review')
    op.create_foreign_key("bill_review_bill_id_fkey", 'bill_review', 'bill', ['bill_id'], ['id'])
    op.drop_constraint("bill_withdrawal_bill_id_fkey", 'bill_withdrawal')
    op.create_foreign_key("bill_withdrawal_bill_id_fkey", 'bill_withdrawal', 'bill', ['bill_id'], ['id'])
    op.drop_constraint("cosponsorship_bill_id_fkey", 'cosponsorship')
    op.create_foreign_key("cosponsorship_bill_id_fkey", 'cosponsorship', 'bill', ['bill_id'], ['id'])
