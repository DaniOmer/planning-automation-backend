"""Merge multiple heads

Revision ID: 6d72e16c107a
Revises: 1352d553575e, 58dbce333d53, d8208c15e571
Create Date: 2024-12-11 18:21:29.446313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d72e16c107a'
down_revision: Union[str, None] = ('1352d553575e', '58dbce333d53', 'd8208c15e571')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
