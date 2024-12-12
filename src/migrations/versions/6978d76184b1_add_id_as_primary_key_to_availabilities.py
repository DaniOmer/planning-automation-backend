"""Add id as primary key to availabilities

Revision ID: 6978d76184b1
Revises: d0297b3bbb4f
Create Date: 2024-12-11 20:01:18.371084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6978d76184b1'
down_revision: Union[str, None] = 'd0297b3bbb4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Supprimer la clé primaire existante (sur users_id)
    op.drop_constraint('availabilities_pkey', 'availabilities', type_='primary')
    # Ajouter une nouvelle colonne id avec clé primaire
    op.add_column('availabilities', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.create_primary_key('pk_availabilities', 'availabilities', ['id'])


def downgrade() -> None:
    # Supprimer la nouvelle clé primaire (sur id)
    op.drop_constraint('pk_availabilities', 'availabilities', type_='primary')
    # Supprimer la colonne id
    op.drop_column('availabilities', 'id')
    # Restaurer la clé primaire originale sur users_id
    op.create_primary_key('availabilities_pkey', 'availabilities', ['users_id'])
