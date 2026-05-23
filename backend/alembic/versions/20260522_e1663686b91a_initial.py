"""
Description: Database migration — initial.
Last Modified By: bvela
Created: 2026-05-22
Last Modified:
    2026-05-22 - Migration created.
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = 'e1663686b91a'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
