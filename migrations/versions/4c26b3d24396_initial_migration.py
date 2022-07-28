"""initial migration

Revision ID: 4c26b3d24396
Revises: 
Create Date: 2022-03-26 14:09:11.974826

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '4c26b3d24396'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_option',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_event_option')),
    sa.UniqueConstraint('name', name=op.f('uq_event_option_name'))
    )
    op.create_table('outcome',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_outcome'))
    )
    op.create_table('role',
    sa.Column('permissions', sa.UnicodeText(), nullable=True),
    sa.Column('update_datetime', sa.DateTime(), server_default=func.now(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_role')),
    sa.UniqueConstraint('name', name=op.f('uq_role_name'))
    )
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('colour', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_team')),
    sa.UniqueConstraint('name', name=op.f('uq_team_name'))
    )
    op.create_table('user',
    sa.Column('fs_uniquifier', sa.String(length=64), nullable=False),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=64), nullable=True),
    sa.Column('current_login_ip', sa.String(length=64), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.Column('tf_primary_method', sa.String(length=64), nullable=True),
    sa.Column('tf_totp_secret', sa.String(length=255), nullable=True),
    sa.Column('tf_phone_number', sa.String(length=128), nullable=True),
    sa.Column('create_datetime', sa.DateTime(), server_default=func.now(), nullable=False),
    sa.Column('update_datetime', sa.DateTime(), server_default=func.now(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('us_totp_secrets', sa.Text(), nullable=True),
    sa.Column('us_phone_number', sa.String(length=128), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('email', name=op.f('uq_user_email')),
    sa.UniqueConstraint('fs_uniquifier', name=op.f('uq_user_fs_uniquifier')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('home_team_id', sa.Integer(), nullable=True),
    sa.Column('away_team_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['away_team_id'], ['team.id'], name=op.f('fk_game_away_team_id_team')),
    sa.ForeignKeyConstraint(['home_team_id'], ['team.id'], name=op.f('fk_game_home_team_id_team')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_game_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_game'))
    )
    op.create_table('outcome_to_event_option',
    sa.Column('outcome_id', sa.Integer(), nullable=True),
    sa.Column('event_option_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_option_id'], ['event_option.id'], name=op.f('fk_outcome_to_event_option_event_option_id_event_option')),
    sa.ForeignKeyConstraint(['outcome_id'], ['outcome.id'], name=op.f('fk_outcome_to_event_option_outcome_id_outcome'))
    )
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], name=op.f('fk_player_team_id_team')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_player'))
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name=op.f('fk_roles_users_role_id_role')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_roles_users_user_id_user'))
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('event_option_id', sa.Integer(), nullable=True),
    sa.Column('outcome_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.String(length=10), nullable=True),
    sa.Column('pitchzone', sa.String(length=10), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_option_id'], ['event_option.id'], name=op.f('fk_event_event_option_id_event_option')),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], name=op.f('fk_event_game_id_game')),
    sa.ForeignKeyConstraint(['outcome_id'], ['outcome.id'], name=op.f('fk_event_outcome_id_outcome')),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], name=op.f('fk_event_team_id_team')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_event'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event')
    op.drop_table('roles_users')
    op.drop_table('player')
    op.drop_table('outcome_to_event_option')
    op.drop_table('game')
    op.drop_table('user')
    op.drop_table('team')
    op.drop_table('role')
    op.drop_table('outcome')
    op.drop_table('event_option')
    # ### end Alembic commands ###
