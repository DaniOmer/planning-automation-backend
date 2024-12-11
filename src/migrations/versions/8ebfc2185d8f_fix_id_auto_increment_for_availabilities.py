"""Fix id auto increment for availabilities

Revision ID: 8ebfc2185d8f
Revises: 5bc4faf4f599
Create Date: 2024-12-11 20:13:13.780558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ebfc2185d8f'
down_revision: Union[str, None] = '5bc4faf4f599'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE SEQUENCE IF NOT EXISTS availabilities_id_seq START WITH 1 INCREMENT BY 1')
    op.execute("ALTER TABLE availabilities ALTER COLUMN id SET DEFAULT nextval('availabilities_id_seq')")

def downgrade() -> None:
    op.execute("ALTER TABLE availabilities ALTER COLUMN id DROP DEFAULT")
    op.execute('DROP SEQUENCE IF EXISTS availabilities_id_seq')