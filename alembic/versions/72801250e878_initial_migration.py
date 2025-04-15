"""Initial migration

Revision ID: 72801250e878
Revises: 0803c3ec415a
Create Date: 2025-03-01 12:30:27.924774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72801250e878'
down_revision: Union[str, None] = '0803c3ec415a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'tickets', ['id'])
    op.drop_constraint('tickets_seat_id_fkey', 'tickets', type_='foreignkey')
    op.drop_constraint('tickets_user_id_fkey', 'tickets', type_='foreignkey')
    op.drop_constraint('tickets_reservation_id_fkey', 'tickets', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('tickets_reservation_id_fkey', 'tickets', 'reservations', ['reservation_id'], ['id'])
    op.create_foreign_key('tickets_user_id_fkey', 'tickets', 'users', ['user_id'], ['id'])
    op.create_foreign_key('tickets_seat_id_fkey', 'tickets', 'seats', ['seat_id'], ['id'])
    op.drop_constraint(None, 'tickets', type_='unique')
    # ### end Alembic commands ###
