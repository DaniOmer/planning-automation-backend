"""Create table availabilities and subjects

Revision ID: 58dbce333d53
Revises: 37e92dd165df
Create Date: 2024-12-11 17:17:10.174289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58dbce333d53'
down_revision: Union[str, None] = '37e92dd165df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subjects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=45), nullable=False),
    sa.Column('hourly_volume', sa.Integer(), nullable=True),
    sa.Column('session_duration', sa.Float(), nullable=True),
    sa.Column('start_at', sa.Date(), nullable=True),
    sa.Column('end_at', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('availabilities',
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=1000), nullable=True),
    sa.Column('start_at', sa.DateTime(), nullable=False),
    sa.Column('end_at', sa.DateTime(), nullable=False),
    sa.Column('is_recurring', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['users_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('users_id')
    )
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=255),
               nullable=False)
    op.create_unique_constraint(None, 'user', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.alter_column('user', 'password',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_table('availabilities')
    op.drop_table('subjects')
    # ### end Alembic commands ###