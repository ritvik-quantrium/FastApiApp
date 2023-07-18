"""Add Last few Columns to post

Revision ID: 509a035aed24
Revises: 2826e9da4de7
Create Date: 2023-07-18 15:50:25.551948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '509a035aed24'
down_revision = '2826e9da4de7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("post" , sa.Column("published" , sa.Boolean() , nullable = False , server_default = "TRUE"))
    op.add_column("post",sa.Column("created_at" , sa.TIMESTAMP(timezone=True) , nullable = False , server_default = sa.text("NOW()")) )


def downgrade() -> None:
    op.drop_column("post" , "published")
    op.drop_column("post" , "created_at")
    pass
