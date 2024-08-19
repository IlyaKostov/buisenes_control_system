"""initial

Revision ID: aa903d560cfb
Revises: 
Create Date: 2024-08-19 15:40:23.936707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa903d560cfb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_account')),
    sa.UniqueConstraint('email', name=op.f('uq_account_email'))
    )
    op.create_table('company',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('inn', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=256), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_company'))
    )
    op.create_table('invite',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], name=op.f('fk_invite_account_id_account')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_invite')),
    sa.UniqueConstraint('account_id', name=op.f('uq_invite_account_id'))
    )
    op.create_table('secret',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], name=op.f('fk_secret_account_id_account')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_secret')),
    sa.UniqueConstraint('account_id', name=op.f('uq_secret_account_id'))
    )
    op.create_table('user',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('middle_name', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], name=op.f('fk_user_account_id_account')),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], name=op.f('fk_user_company_id_company'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('account_id', name=op.f('uq_user_account_id'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('secret')
    op.drop_table('invite')
    op.drop_table('company')
    op.drop_table('account')
    # ### end Alembic commands ###
