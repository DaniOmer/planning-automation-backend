"""Merge heads 37db3d4ad11a and f9a06dd0cace

Revision ID: a0f5c81b597a
Revises: 37db3d4ad11a, f9a06dd0cace
Create Date: 2024-12-14 00:41:51.182420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0f5c81b597a'
down_revision: Union[str, None] = ('37db3d4ad11a', 'f9a06dd0cace')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
