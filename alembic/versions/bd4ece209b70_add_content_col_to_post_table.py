"""Add content col to Post table

Revision ID: bd4ece209b70
Revises: 46beee29bce7
Create Date: 2024-11-18 19:34:04.140993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd4ece209b70'
down_revision: Union[str, None] = '46beee29bce7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
