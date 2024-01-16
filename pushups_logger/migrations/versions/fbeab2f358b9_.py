"""empty message

Revision ID: fbeab2f358b9
Revises: 
Create Date: 2023-12-11 21:00:30.849040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbeab2f358b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('weight', sa.Integer()))
        batch_op.add_column(sa.Column('size', sa.Integer()))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('size')
        batch_op.drop_column('weight')

    # ### end Alembic commands ###