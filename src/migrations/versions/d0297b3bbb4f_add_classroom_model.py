"""Add classroom model

Revision ID: d0297b3bbb4f
Revises: 6d72e16c107a
Create Date: 2024-12-11 18:21:52.214522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0297b3bbb4f'
down_revision: Union[str, None] = '6d72e16c107a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classrooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=45), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_classrooms_id'), 'classrooms', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_classrooms_id'), table_name='classrooms')
    op.drop_table('classrooms')
    # ### end Alembic commands ###
