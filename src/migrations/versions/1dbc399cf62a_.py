"""empty message

Revision ID: 1dbc399cf62a
Revises: 97f7f6c19239, f7702c74ea64
Create Date: 2024-12-12 14:16:53.410441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1dbc399cf62a'
down_revision: Union[str, None] = ('97f7f6c19239', 'f7702c74ea64')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
