"""empty message

Revision ID: cb0bb21c55cc
Revises: 
Create Date: 2022-12-20 05:36:03.949289

"""
import os
import json

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb0bb21c55cc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    users = op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    with open(os.path.join(os.path.dirname(__file__), "../data/users.json")) as f:
        user_data = f.read()

    op.bulk_insert(users, json.loads(user_data))
    
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###