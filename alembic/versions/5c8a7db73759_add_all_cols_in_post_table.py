"""add all cols in post table

Revision ID: 5c8a7db73759
Revises: 13d0399e99a3
Create Date: 2024-11-18 19:53:26.694309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c8a7db73759'
down_revision: Union[str, None] = '13d0399e99a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published',sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
