"""create ingredient_quantities table

Revision ID: 31e69f731f7c
Revises: 76b68abd9f65
Create Date: 2023-05-21 23:56:25.601423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31e69f731f7c'
down_revision = '76b68abd9f65'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'ingredient_quantities',
        sa.Column('recipe_id', sa.Integer, primary_key=True),
        sa.Column('ingredient_id', sa.Integer, primary_key=True),
        sa.Column('amount', sa.String(50), nullable=True),
        sa.Column('unit_type', sa.String(50), nullable=True),
        sa.Column('ingredient_price_usd', sa.Float(50), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('ingredient_quantities')
