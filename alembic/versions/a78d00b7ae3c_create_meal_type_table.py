"""create meal_type table

Revision ID: a78d00b7ae3c
Revises: 
Create Date: 2023-05-21 11:18:18.291687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a78d00b7ae3c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'meal_type',
        sa.Column('meal_type_id', sa.Integer, primary_key=True),
        sa.Column('meal_type', sa.String(50), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('meal_type')
