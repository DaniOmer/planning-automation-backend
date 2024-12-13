"""move day_type from table educational_courses to years_groups_has_educational_courses

Revision ID: f9a06dd0cace
Revises: 25da8d84384a
Create Date: 2024-12-13 11:28:55.355967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9a06dd0cace'
down_revision: Union[str, None] = '25da8d84384a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('educational_courses', 'day_type')
    op.add_column('years_groups_educational_courses', sa.Column('day_type', sa.String(length=255), nullable=False))
    op.drop_constraint('years_groups_educational_courses_day_type_id_fkey', 'years_groups_educational_courses', type_='foreignkey')
    op.drop_column('years_groups_educational_courses', 'day_type_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('years_groups_educational_courses', sa.Column('day_type_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('years_groups_educational_courses_day_type_id_fkey', 'years_groups_educational_courses', 'day_type', ['day_type_id'], ['id'])
    op.drop_column('years_groups_educational_courses', 'day_type')
    op.add_column('educational_courses', sa.Column('day_type', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    # ### end Alembic commands ###