"""empty message

Revision ID: 35a5734649ff
Revises: 
Create Date: 2020-08-18 08:01:49.098420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35a5734649ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('price', sa.String(length=15), nullable=True),
    sa.Column('type', sa.String(length=100), nullable=True),
    sa.Column('uniqueid', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('items')
    # ### end Alembic commands ###
