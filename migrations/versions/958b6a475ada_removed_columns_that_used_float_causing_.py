"""removed columns that used float, causing conflicts 



Revision ID: 958b6a475ada
Revises: 6d62071d245a
Create Date: 2023-09-10 09:43:58.630593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '958b6a475ada'
down_revision = '6d62071d245a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('overview', schema=None) as batch_op:
        batch_op.alter_column('load_capacity_tonnes',
               existing_type=sa.FLOAT(),
               type_=sa.String(length=100),
               existing_nullable=True)
        batch_op.alter_column('idle_percentage',
               existing_type=sa.FLOAT(),
               type_=sa.String(length=100),
               existing_nullable=True)
        batch_op.alter_column('utilisation_percentage',
               existing_type=sa.FLOAT(),
               type_=sa.String(length=100),
               existing_nullable=True)
        batch_op.alter_column('data_level_percentage',
               existing_type=sa.FLOAT(),
               type_=sa.String(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('overview', schema=None) as batch_op:
        batch_op.alter_column('data_level_percentage',
               existing_type=sa.String(length=100),
               type_=sa.FLOAT(),
               existing_nullable=True)
        batch_op.alter_column('utilisation_percentage',
               existing_type=sa.String(length=100),
               type_=sa.FLOAT(),
               existing_nullable=True)
        batch_op.alter_column('idle_percentage',
               existing_type=sa.String(length=100),
               type_=sa.FLOAT(),
               existing_nullable=True)
        batch_op.alter_column('load_capacity_tonnes',
               existing_type=sa.String(length=100),
               type_=sa.FLOAT(),
               existing_nullable=True)

    # ### end Alembic commands ###
