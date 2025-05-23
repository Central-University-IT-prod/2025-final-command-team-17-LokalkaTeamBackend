"""Initial migration

Revision ID: 6a7815b5acbd
Revises: 7667533afec6
Create Date: 2025-03-02 16:36:50.946694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a7815b5acbd'
down_revision: Union[str, None] = '7667533afec6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('telegram_users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('telegram_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_telegram_users_telegram_id'), 'telegram_users', ['telegram_id'], unique=True)
    op.create_index(op.f('ix_telegram_users_user_id'), 'telegram_users', ['user_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_telegram_users_user_id'), table_name='telegram_users')
    op.drop_index(op.f('ix_telegram_users_telegram_id'), table_name='telegram_users')
    op.drop_table('telegram_users')
    # ### end Alembic commands ###
