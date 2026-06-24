"""
Initial migration - Create users table

Revision ID: 001
Revises:
Create Date: 2026-06-24 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create role enum type
    role_enum = postgresql.ENUM('baker', 'sales', 'hr', 'cofounder', 'admin', name='roleenum')
    role_enum.create(op.get_bind())

    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('hashed_password', sa.String(100), nullable=False),
        sa.Column('full_name', sa.String(100), nullable=False),
        sa.Column('role', sa.Enum('baker', 'sales', 'hr', 'cofounder', 'admin', name='roleenum'), server_default='sales', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )

def downgrade() -> None:
    # Drop users table
    op.drop_table('users')

    # Drop role enum type
    op.execute("DROP TYPE roleenum")