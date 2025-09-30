"""
add auth_sessions table

Revision ID: 97dda666f046
Revises: 333adc2790c7
Create Date: 2025-09-22 08:56:04.109362
"""

# --- IMPORTS ---
from alembic import op
import sqlalchemy as sa


# --- TYPES ---
from typing import Union
from typing import Sequence


# revision identifiers, used by Alembic.
revision: str = '97dda666f046'
down_revision: Union[str, Sequence[str], None] = '333adc2790c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade schema.
    """

    # Create table
    op.create_table(
        'auth_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('jti', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('jti'),
        schema='auth'
    )

    # Create indexes
    op.create_index(op.f('ix_auth_auth_sessions_expires_at'),
                    'auth_sessions', ['expires_at'], unique=False, schema='auth')

    op.create_index(op.f('ix_auth_auth_sessions_user_id'),
                    'auth_sessions', ['user_id'], unique=False, schema='auth')


def downgrade() -> None:
    """
    Downgrade schema.
    """
    raise NotImplementedError('Downgrade is disabled.')
