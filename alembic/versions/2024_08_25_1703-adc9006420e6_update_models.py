"""update models

Revision ID: adc9006420e6
Revises: aa903d560cfb
Create Date: 2024-08-25 17:03:11.780733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'adc9006420e6'
down_revision: Union[str, None] = 'aa903d560cfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('secret', 'password',
                    existing_type=sa.VARCHAR(),
                    type_=sa.LargeBinary(),
                    existing_nullable=False,
                    postgresql_using='password::bytea'
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('secret', 'password',
                    existing_type=sa.LargeBinary(),
                    type_=sa.VARCHAR(),
                    existing_nullable=False)
    # ### end Alembic commands ###
