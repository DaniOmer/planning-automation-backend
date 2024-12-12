"""empty message

Revision ID: fb4af891b9e8
Revises: 1dbc399cf62a, 920703f4e9f5
Create Date: 2024-12-12 15:42:54.617984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb4af891b9e8'
down_revision: Union[str, None] = ('1dbc399cf62a', '920703f4e9f5')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
