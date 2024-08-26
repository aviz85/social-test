"""Add raw_content and rendered_content to Post model

Revision ID: 961d5d679df1
Revises: 
Create Date: 2024-08-26 17:32:29.529743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '961d5d679df1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('raw_content', sa.Text(), nullable=False))
    op.add_column('post', sa.Column('rendered_content', sa.Text(), nullable=False))
    op.drop_column('post', 'content')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('content', sa.TEXT(), nullable=False))
    op.drop_column('post', 'rendered_content')
    op.drop_column('post', 'raw_content')
    # ### end Alembic commands ###
