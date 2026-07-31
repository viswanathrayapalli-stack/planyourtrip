"""create_places_table

Revision ID: b00664bb6c92
Revises: 58ffdcc0266d
Create Date: 2026-07-31 12:05:47.262270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b00664bb6c92"
down_revision: Union[str, Sequence[str], None] = "58ffdcc0266d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "places",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("place_type", sa.String(length=50), nullable=True),
        sa.Column("destination_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["destination_id"],
            ["destinations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Index to improve lookups by destination
    op.create_index(
        "ix_places_destination_id",
        "places",
        ["destination_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "ix_places_destination_id",
        table_name="places",
    )

    op.drop_table("places")