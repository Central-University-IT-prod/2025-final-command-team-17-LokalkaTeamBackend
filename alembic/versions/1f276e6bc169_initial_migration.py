"""Initial migration

Revision ID: 1f276e6bc169
Revises: 00810662eab7
Create Date: 2025-03-01 21:43:27.273213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f276e6bc169'
down_revision: Union[str, None] = '00810662eab7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservations', sa.Column('status', sa.String(), nullable=False))
    op.add_column('tickets', sa.Column('made_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tickets', 'made_on')
    op.drop_column('reservations', 'status')
    # ### end Alembic commands ###
