"""Rename assignments_courses to assignments_subjects and update column names

Revision ID: 920703f4e9f5
Revises: 97f7f6c19239
Create Date: 2024-12-12 15:20:08.760025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '920703f4e9f5'
down_revision: Union[str, None] = '97f7f6c19239'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assignments_subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('classes_id', sa.Integer(), nullable=False),
    sa.Column('subjects_id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.Column('url_online', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['classes_id'], ['classes.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['subjects_id'], ['subjects.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['users_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assignments_subjects_id'), 'assignments_subjects', ['id'], unique=False)
    op.drop_index('ix_assignments_courses_id', table_name='assignments_courses')
    op.drop_table('assignments_courses')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assignments_courses',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('classes_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('courses_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('users_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('url_online', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['classes_id'], ['classes.id'], name='assignments_courses_classes_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['courses_id'], ['subjects.id'], name='assignments_courses_courses_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['users_id'], ['user.id'], name='assignments_courses_users_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='assignments_courses_pkey')
    )
    op.create_index('ix_assignments_courses_id', 'assignments_courses', ['id'], unique=False)
    op.drop_index(op.f('ix_assignments_subjects_id'), table_name='assignments_subjects')
    op.drop_table('assignments_subjects')
    # ### end Alembic commands ###