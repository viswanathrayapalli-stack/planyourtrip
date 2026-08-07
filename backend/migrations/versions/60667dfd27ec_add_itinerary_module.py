"""add itinerary module

Revision ID: 60667dfd27ec
Revises: b00664bb6c92
Create Date: 2026-07-31 15:50:24.323149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "60667dfd27ec"
down_revision: Union[str, Sequence[str], None] = "b00664bb6c92"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "itineraries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("day_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
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
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "trip_id",
            "day_number",
            name="uq_itinerary_trip_day",
        ),
    )

    op.create_table(
        "itinerary_activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("itinerary_id", sa.Integer(), nullable=False),
        sa.Column("place_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("activity_order", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=True),
        sa.Column("end_time", sa.Time(), nullable=True),
        sa.Column("estimated_duration_minutes", sa.Integer(), nullable=True),
        sa.Column("transport_mode", sa.String(length=50), nullable=True),
        sa.Column(
            "estimated_cost",
            sa.Numeric(precision=10, scale=2),
            nullable=True,
        ),
        sa.Column("notes", sa.Text(), nullable=True),
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
        sa.ForeignKeyConstraint(["itinerary_id"], ["itineraries.id"]),
        sa.ForeignKeyConstraint(["place_id"], ["places.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "itinerary_id",
            "activity_order",
            name="uq_itinerary_activity_order",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("itinerary_activities")
    op.drop_table("itineraries")