"""empty message

Revision ID: 4dceb881d61a
Revises: 5319a27cf316
Create Date: 2014-02-13 23:53:12.585454

"""

# revision identifiers, used by Alembic.
revision = '4dceb881d61a'
down_revision = '5319a27cf316'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_verified')
    ### end Alembic commands ###