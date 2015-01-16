"""product and picture

Revision ID: 164e05aa3e84
Revises: 2e4fb5b3a97
Create Date: 2015-01-16 11:54:09.927322

"""

# revision identifiers, used by Alembic.
revision = '164e05aa3e84'
down_revision = '2e4fb5b3a97'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('picture',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('width', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('filename', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('instock', sa.Boolean(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_pics',
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('picture_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['picture_id'], ['picture.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_pics')
    op.drop_table('product')
    op.drop_table('picture')
    ### end Alembic commands ###