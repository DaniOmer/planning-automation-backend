"""Merge heads

Revision ID: 0fe65c4999a0
Revises: 37db3d4ad11a, f9a06dd0cace
Create Date: 2024-12-13 15:40:44.120516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fe65c4999a0'
down_revision: Union[str, None] = ('37db3d4ad11a', 'f9a06dd0cace')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
