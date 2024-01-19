"""add content column

Revision ID: 28fee053ed84
Revises: 5b3321b9322d
Create Date: 2024-01-19 14:21:02.953949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28fee053ed84'
down_revision: Union[str, None] = '5b3321b9322d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
