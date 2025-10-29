"""Rename metadata to meta_data in bot_interactions

Revision ID: c1d2e3f4g5h6
Revises: b1c2d3e4f5a6
Create Date: 2025-10-29 15:50:00.000000+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1d2e3f4g5h6'
down_revision = 'b1c2d3e4f5a6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename metadata column to meta_data in bot_interactions table
    op.alter_column('bot_interactions', 'metadata', new_column_name='meta_data')


def downgrade() -> None:
    # Rename back meta_data to metadata
    op.alter_column('bot_interactions', 'meta_data', new_column_name='metadata')
