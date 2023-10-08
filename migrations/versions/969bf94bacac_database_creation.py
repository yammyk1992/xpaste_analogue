"""Database Creation

Revision ID: 969bf94bacac
Revises: 
Create Date: 2023-10-08 18:31:09.423987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '969bf94bacac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('text_create',
                    sa.Column('text_uuid', sa.UUID(), nullable=False),
                    sa.Column('text', sa.String(length=255), nullable=False),
                    sa.Column('salt', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('text_uuid'),
                    sa.UniqueConstraint('text_uuid')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('text_create')
    # ### end Alembic commands ###