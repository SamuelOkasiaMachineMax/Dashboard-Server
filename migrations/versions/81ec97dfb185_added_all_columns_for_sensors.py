"""added all columns for sensors

Revision ID: 81ec97dfb185
Revises: 116309d3209a
Create Date: 2023-09-09 10:58:15.685664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81ec97dfb185'
down_revision = '116309d3209a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sensor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('latest_connection', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('data_completion', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('latest_hours', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('latest_latitude', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('latest_location_timestamp', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('site', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('firmware_version', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('configuration_version', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('device_mode', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('first_associated', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('signal', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sensor', schema=None) as batch_op:
        batch_op.drop_column('signal')
        batch_op.drop_column('first_associated')
        batch_op.drop_column('device_mode')
        batch_op.drop_column('configuration_version')
        batch_op.drop_column('firmware_version')
        batch_op.drop_column('site')
        batch_op.drop_column('latest_location_timestamp')
        batch_op.drop_column('latest_latitude')
        batch_op.drop_column('latest_hours')
        batch_op.drop_column('data_completion')
        batch_op.drop_column('latest_connection')

    # ### end Alembic commands ###