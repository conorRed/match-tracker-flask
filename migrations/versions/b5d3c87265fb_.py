"""empty message

Revision ID: b5d3c87265fb
Revises: 4c26b3d24396
Create Date: 2022-03-26 14:31:28.379314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5d3c87265fb'
down_revision = '4c26b3d24396'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint('fk_event_game_id_game', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_event_game_id_game'), 'game', ['game_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_event_game_id_game'), type_='foreignkey')
        batch_op.create_foreign_key('fk_event_game_id_game', 'game', ['game_id'], ['id'])

    # ### end Alembic commands ###