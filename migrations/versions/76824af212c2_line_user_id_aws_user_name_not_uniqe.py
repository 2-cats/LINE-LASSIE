"""line_user_id aws_user_name not uniqe

Revision ID: 76824af212c2
Revises: 216d42d7a4f4
Create Date: 2019-03-06 13:42:38.393511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76824af212c2'
down_revision = '216d42d7a4f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('aws_user_name', table_name='users')
    op.drop_index('line_user_id', table_name='users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('line_user_id', 'users', ['line_user_id'], unique=True)
    op.create_index('aws_user_name', 'users', ['aws_user_name'], unique=True)
    # ### end Alembic commands ###