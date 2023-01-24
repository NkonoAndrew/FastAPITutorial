"""create posts table

Revision ID: 4d3f7bdf632e
Revises: 339f9ea06f7c
Create Date: 2023-01-23 14:16:41.632909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d3f7bdf632e'
down_revision = '339f9ea06f7c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), nullable=False, server_default ='TRUE'),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
