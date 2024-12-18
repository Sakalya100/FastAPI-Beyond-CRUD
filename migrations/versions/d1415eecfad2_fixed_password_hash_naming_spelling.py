"""fixed password_hash naming spelling”

Revision ID: d1415eecfad2
Revises: 40f0ee25b540
Create Date: 2024-11-10 01:34:21.018570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 


# revision identifiers, used by Alembic.
revision: str = 'd1415eecfad2'
down_revision: Union[str, None] = '40f0ee25b540'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.drop_column('users', 'pasword_hash')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('pasword_hash', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###
