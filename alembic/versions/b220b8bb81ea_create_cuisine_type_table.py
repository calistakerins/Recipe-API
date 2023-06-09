"""create cuisine_type table

Revision ID: b220b8bb81ea
Revises: a78d00b7ae3c
Create Date: 2023-05-21 23:44:49.245304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b220b8bb81ea'
down_revision = 'a78d00b7ae3c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'cuisine_type',
        sa.Column('cuisine_type_id', sa.Integer, primary_key=True),
        sa.Column('cuisine_type', sa.String(50), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('cuisine_type')
