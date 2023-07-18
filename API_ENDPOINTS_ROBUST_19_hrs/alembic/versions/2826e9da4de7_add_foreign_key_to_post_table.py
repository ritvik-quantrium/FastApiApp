"""Add Foreign_key to post Table

Revision ID: 2826e9da4de7
Revises: 3271ea88f089
Create Date: 2023-07-18 15:33:31.259372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2826e9da4de7'
down_revision = '3271ea88f089'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("post" , sa.Column("owner_id" , sa.Integer() , nullable = False))
    op.create_foreign_key("Post_users_FK" , source_table="post" , referent_table="users" , local_cols=["owner_id"] , remote_cols=["id"] , ondelete="CASCADE")

    pass


def downgrade() -> None:
    op.drop_constraint("Post_users_FK" , table_name="post")
    op.drop_column("post" , "owner_id")
    pass
