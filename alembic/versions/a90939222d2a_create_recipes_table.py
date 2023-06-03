"""create recipes table

Revision ID: a90939222d2a
Revises: ef9243012fd0
Create Date: 2023-05-22 00:05:17.011778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a90939222d2a'
down_revision = 'ef9243012fd0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'recipes',
        sa.Column('recipe_id', sa.Integer, primary_key=True),
        sa.Column('recipe_name', sa.String(50), nullable=False),
        sa.Column('calories', sa.Integer, nullable=True),
        sa.Column('prep_time_mins', sa.Integer, nullable=True),
        sa.Column('recipe_instructions', sa.String(50), nullable=True),
        sa.Column('recipe_url', sa.String(50), nullable=True),
        sa.Column('number_of_favorites', sa.Integer, nullable=True),

    )


def downgrade() -> None:
    op.drop_table('recipes')
