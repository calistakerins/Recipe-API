"""create recipe_meal_types table

Revision ID: ef9243012fd0
Revises: 92c4f1601e28
Create Date: 2023-05-22 00:04:00.740781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef9243012fd0'
down_revision = '92c4f1601e28'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'recipe_meal_types',
        sa.Column('recipe_id', sa.Integer, primary_key=True),
        sa.Column('meal_type_id', sa.Integer, primary_key=True),
    )


def downgrade() -> None:
    op.drop_table('recipe_meal_types')
