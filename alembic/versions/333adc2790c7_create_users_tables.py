"""
create users tables

Revision ID: 333adc2790c7
Revises: 
Create Date: 2025-09-09 21:15:59.845041
"""

# --- IMPORTS ---
from alembic import op
import sqlalchemy as sa


# --- TYPES ---
from typing import Union
from typing import Sequence


# revision identifiers, used by Alembic.
revision: str = '333adc2790c7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade schema.
    """

    # Ensure the schema exists before creating the table
    op.execute('CREATE SCHEMA IF NOT EXISTS auth')

    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('USER', 'ADMIN', name='user_role_enum', schema='auth'), nullable=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='auth'
    )


def downgrade() -> None:
    """
    Downgrade schema.
    """
    raise NotImplementedError('Downgrade is disabled.')
