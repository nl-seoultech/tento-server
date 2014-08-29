"""Add Position

Revision ID: 4ee2d02f091
Revises: 4ad3f96f41b
Create Date: 2014-08-26 17:52:03.089830

"""

# revision identifiers, used by Alembic.
revision = '4ee2d02f091'
down_revision = '4ad3f96f41b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('positions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('x', sa.Float(), nullable=False),
    sa.Column('y', sa.Float(), nullable=False),
    sa.Column('music_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['music_id'], ['musics.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('positions')
    ### end Alembic commands ###