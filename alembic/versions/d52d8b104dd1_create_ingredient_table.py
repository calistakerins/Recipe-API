"""create ingredient table

Revision ID: d52d8b104dd1
Revises: 31e69f731f7c
Create Date: 2023-05-21 23:59:59.829550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd52d8b104dd1'
down_revision = '31e69f731f7c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'ingredients',
        sa.Column('ingredient_id', sa.Integer, primary_key=True),
        sa.Column('ingredient_name', sa.String(50), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('ingredient')
