"""Add uuid

Revision ID: 5645a20a30f7
Revises: 
Create Date: 2023-09-27 10:56:02.321975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5645a20a30f7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('text_create',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('text', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('salt', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('text_create')
    # ### end Alembic commands ###