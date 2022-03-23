"""add outcome relationship to event model

Revision ID: 8e748614e4ec
Revises: 4f26ae246f2f
Create Date: 2022-02-09 13:22:16.074690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e748614e4ec'
down_revision = '80906fc5ad07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('outcome_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_event_outcome_id_outcome'), 'outcome', ['outcome_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_event_outcome_id_outcome'), type_='foreignkey')
        batch_op.drop_column('outcome_id')

    # ### end Alembic commands ###