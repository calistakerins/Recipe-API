"""create users table

Revision ID: 1740b8fd4eb5
Revises: a90939222d2a
Create Date: 2023-05-22 00:09:11.254580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1740b8fd4eb5'
down_revision = 'a90939222d2a'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, primary_key=True),
        sa.Column('user_name', sa.String(50), nullable=False),
        sa.Column('password', sa.String(50), nullable=False)

    )


def downgrade() -> None:
    op.drop_table('users')
