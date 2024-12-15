"""Merge heads 0fe65c4999a0 and a0f5c81b597a

Revision ID: 95f52e16b279
Revises: 0fe65c4999a0, a0f5c81b597a
Create Date: 2024-12-14 09:38:09.905907

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95f52e16b279'
down_revision: Union[str, None] = ('0fe65c4999a0', 'a0f5c81b597a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
