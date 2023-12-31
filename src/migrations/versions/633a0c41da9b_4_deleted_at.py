"""4_deleted_at

Revision ID: 633a0c41da9b
Revises: 54733a8eacd2
Create Date: 2023-10-02 17:39:39.767653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '633a0c41da9b'
down_revision: Union[str, None] = '54733a8eacd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('deleted_at')

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('deleted_at')

    # ### end Alembic commands ###
