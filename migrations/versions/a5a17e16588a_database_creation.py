"""Database Creation

Revision ID: a5a17e16588a
Revises: 
Create Date: 2023-10-01 23:51:22.939441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a5a17e16588a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('text_create',
                    sa.Column('text_uuid', sa.UUID(), nullable=False),
                    sa.Column('schemas', sa.String(length=255), nullable=False),
                    sa.Column('salt', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('text_uuid'),
                    sa.UniqueConstraint('text_uuid')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('text_create')
    # ### end Alembic commands ###
