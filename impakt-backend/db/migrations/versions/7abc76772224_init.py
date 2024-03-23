"""init

Revision ID: 7abc76772224
Revises: 
Create Date: 2024-03-23 19:47:49.687041+08:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7abc76772224"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Company",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("stock_ticker", sa.String(), nullable=True),
        sa.Column("website", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "Sdg",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "CompanyInitiative",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("key_stats", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("date", sa.DateTime(), nullable=True),
        sa.Column(
            "impact",
            sa.Enum("LOW", "MEDIUM", "HIGH", name="impact"),
            nullable=True,
        ),
        sa.Column("justification", sa.String(), nullable=True),
        sa.Column("source", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["Company.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "SubSdg",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sdg_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["sdg_id"],
            ["Sdg.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "CompanyInitiativeSubSdg",
        sa.Column("initiative_id", sa.Integer(), nullable=False),
        sa.Column("sub_sdg_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["initiative_id"],
            ["CompanyInitiative.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sub_sdg_id"],
            ["SubSdg.id"],
        ),
        sa.PrimaryKeyConstraint("initiative_id", "sub_sdg_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("CompanyInitiativeSubSdg")
    op.drop_table("SubSdg")
    op.drop_table("CompanyInitiative")
    op.drop_table("Sdg")
    op.drop_table("Company")
    # ### end Alembic commands ###