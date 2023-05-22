"""create recipe_cuisine_types table

Revision ID: 92c4f1601e28
Revises: d52d8b104dd1
Create Date: 2023-05-22 00:01:35.547161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92c4f1601e28'
down_revision = 'd52d8b104dd1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'recipe_cuisine_types',
        sa.Column('recipe_id', sa.Integer, primary_key=True),
        sa.Column('cuisine_type_id', sa.Integer, primary_key=True),
    )


def downgrade() -> None:
    op.drop_table('recipe_cuisine_types')