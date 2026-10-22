"""add content column to the post table

Revision ID: b8d0a1bd73e3
Revises: 65b1ae2b10a4
Create Date: 2026-08-17 14:28:39.884897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8d0a1bd73e3'
down_revision: Union[str, Sequence[str], None] = '65b1ae2b10a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
