"""Create Post Table

Revision ID: 942cc47a0adb
Revises: 
Create Date: 2023-07-18 14:05:20.590588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '942cc47a0adb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("post" , sa.Column("id" , sa.Integer(),nullable=False , primary_key = True) 
                    ,sa.Column("title" , sa.String() , nullable = False )
                    )

    pass


def downgrade() -> None:
    op.drop_table("post")
    pass
