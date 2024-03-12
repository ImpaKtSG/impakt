"""test

Revision ID: 8b5424ef14c4
Revises: 
Create Date: 2024-03-12 11:33:21.023575+08:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8b5424ef14c4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "company",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("stock_ticker", sa.String(), nullable=True),
        sa.Column("website", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "companydescription",
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["company.id"],
        ),
        sa.PrimaryKeyConstraint("company_id", "description"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("companydescription")
    op.drop_table("company")
    # ### end Alembic commands ###
