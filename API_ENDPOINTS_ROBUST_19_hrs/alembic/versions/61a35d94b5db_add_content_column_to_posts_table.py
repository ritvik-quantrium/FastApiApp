"""Add content Column to posts Table

Revision ID: 61a35d94b5db
Revises: 942cc47a0adb
Create Date: 2023-07-18 15:07:45.778004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61a35d94b5db'
down_revision = '942cc47a0adb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("post" , sa.Column("content" , sa.String() , nullable = False))
    pass


def downgrade() -> None:
    op.drop_column("post" , "content")
    pass
