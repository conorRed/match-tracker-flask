"""empty message

Revision ID: 3066834ccddf
Revises: 8590a8b22368
Create Date: 2022-03-28 14:11:24.476028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3066834ccddf'
down_revision = '8590a8b22368'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('outcome_to_event_option', schema=None) as batch_op:
        batch_op.drop_constraint('fk_outcome_to_event_option_event_option_id_event_option', type_='foreignkey')
        batch_op.drop_constraint('fk_outcome_to_event_option_outcome_id_outcome', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_outcome_to_event_option_event_option_id_event_option'), 'event_option', ['event_option_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(batch_op.f('fk_outcome_to_event_option_outcome_id_outcome'), 'outcome', ['outcome_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('outcome_to_event_option', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_outcome_to_event_option_outcome_id_outcome'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_outcome_to_event_option_event_option_id_event_option'), type_='foreignkey')
        batch_op.create_foreign_key('fk_outcome_to_event_option_outcome_id_outcome', 'outcome', ['outcome_id'], ['id'])
        batch_op.create_foreign_key('fk_outcome_to_event_option_event_option_id_event_option', 'event_option', ['event_option_id'], ['id'])

    # ### end Alembic commands ###
