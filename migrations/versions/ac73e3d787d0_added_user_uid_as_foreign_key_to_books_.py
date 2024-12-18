"""Added user.uid as foreign key to books table

Revision ID: ac73e3d787d0
Revises: 22711c3b4279
Create Date: 2024-11-10 19:36:35.559283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 


# revision identifiers, used by Alembic.
revision: str = 'ac73e3d787d0'
down_revision: Union[str, None] = '22711c3b4279'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('user_uid', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'books', 'users', ['user_uid'], ['uid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_column('books', 'user_uid')
    # ### end Alembic commands ###
