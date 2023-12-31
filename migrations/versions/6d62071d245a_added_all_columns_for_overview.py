"""added all columns for overview

Revision ID: 6d62071d245a
Revises: 85a603e73bb2
Create Date: 2023-09-10 09:30:09.020910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d62071d245a'
down_revision = '85a603e73bb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('overview', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_date', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('end_date', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('load_capacity_tonnes', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('manufacturing_year', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('engine_type', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('emission_standard', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('site', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('active_time', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('idle_time', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('total_on_time', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('off_time', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('data_completeness', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('idle_percentage', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('utilisation_percentage', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('data_level_percentage', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('telematics_found', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('activity_data_source', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('location_data_source', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('hour_meter_data_source', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('ownership_type', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('owner', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('note', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('subscriptions', sa.String(length=100), nullable=True))
        batch_op.drop_column('end_customer')
        batch_op.drop_column('telamatics_found')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('overview', schema=None) as batch_op:
        batch_op.add_column(sa.Column('telamatics_found', sa.VARCHAR(length=100), nullable=True))
        batch_op.add_column(sa.Column('end_customer', sa.VARCHAR(length=100), nullable=True))
        batch_op.drop_column('subscriptions')
        batch_op.drop_column('note')
        batch_op.drop_column('owner')
        batch_op.drop_column('ownership_type')
        batch_op.drop_column('hour_meter_data_source')
        batch_op.drop_column('location_data_source')
        batch_op.drop_column('activity_data_source')
        batch_op.drop_column('telematics_found')
        batch_op.drop_column('data_level_percentage')
        batch_op.drop_column('utilisation_percentage')
        batch_op.drop_column('idle_percentage')
        batch_op.drop_column('data_completeness')
        batch_op.drop_column('off_time')
        batch_op.drop_column('total_on_time')
        batch_op.drop_column('idle_time')
        batch_op.drop_column('active_time')
        batch_op.drop_column('site')
        batch_op.drop_column('emission_standard')
        batch_op.drop_column('engine_type')
        batch_op.drop_column('manufacturing_year')
        batch_op.drop_column('load_capacity_tonnes')
        batch_op.drop_column('end_date')
        batch_op.drop_column('start_date')

    # ### end Alembic commands ###
