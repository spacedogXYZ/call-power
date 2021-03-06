""" Track all calls by user in a session

Revision ID: 3c34cfd19bf8
Revises: 55af52b20fb3
Create Date: 2015-09-15 23:36:21.907575

"""

# revision identifiers, used by Alembic.
revision = '3c34cfd19bf8'
down_revision = '55af52b20fb3'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('calls_session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('campaign_id', sa.Integer(), nullable=True),
    sa.Column('phone_hash', sa.String(length=64), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('from_number', sa.String(length=16), nullable=True),
    sa.Column('twilio_id', sa.String(length=40), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=25), nullable=True),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign_campaign.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table(u'calls', schema=None) as batch_op:
        batch_op.add_column(sa.Column('session_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('calls', 'calls_session', ['session_id'], ['id'])
        batch_op.drop_column('location')
        batch_op.drop_column('phone_hash')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table(u'calls', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_hash', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('location', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('session_id')

    op.drop_table('calls_session')
    ### end Alembic commands ###
