"""added sensor class and overview class

Revision ID: 48ecf7234a27
Revises: 55ff7fb62456
Create Date: 2023-09-05 10:50:01.581884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48ecf7234a27'
down_revision = '55ff7fb62456'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('overview',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('asset_id', sa.String(length=100), nullable=True),
    sa.Column('machine_name', sa.String(length=100), nullable=True),
    sa.Column('machine_type', sa.String(length=100), nullable=True),
    sa.Column('oem', sa.String(length=100), nullable=True),
    sa.Column('model', sa.String(length=100), nullable=True),
    sa.Column('vin', sa.String(length=100), nullable=True),
    sa.Column('end_customer', sa.String(length=100), nullable=True),
    sa.Column('telamatics_found', sa.String(length=100), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sensor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('asset_id', sa.String(length=100), nullable=True),
    sa.Column('machine_name', sa.String(length=100), nullable=True),
    sa.Column('source_status', sa.String(length=100), nullable=True),
    sa.Column('battery_voltage', sa.String(length=100), nullable=True),
    sa.Column('signal_status', sa.String(length=100), nullable=True),
    sa.Column('device_model', sa.String(length=100), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensor')
    op.drop_table('overview')
    # ### end Alembic commands ###