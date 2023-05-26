"""create favorited_recipes table

Revision ID: 76b68abd9f65
Revises: b220b8bb81ea
Create Date: 2023-05-21 23:48:50.265835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76b68abd9f65'
down_revision = 'b220b8bb81ea'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'favorited_recipes',
        sa.Column('recipe_id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, primary_key=True),
        sa.Column('date_favorited', sa.String(50), nullable=True)
    )


def downgrade() -> None:
    op.drop_table('favorited_recipes')

