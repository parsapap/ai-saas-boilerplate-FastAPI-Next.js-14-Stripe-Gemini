"""add ai usage tracking

Revision ID: 004
Revises: 003
Create Date: 2024-12-02

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create ai_usage table
    op.create_table(
        'ai_usage',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('message_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('input_tokens', sa.BigInteger(), nullable=True, server_default='0'),
        sa.Column('output_tokens', sa.BigInteger(), nullable=True, server_default='0'),
        sa.Column('total_tokens', sa.BigInteger(), nullable=True, server_default='0'),
        sa.Column('estimated_cost', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_usage_date'), 'ai_usage', ['date'], unique=False)
    op.create_index(op.f('ix_ai_usage_organization_id'), 'ai_usage', ['organization_id'], unique=False)
    
    # Create ai_requests table
    op.create_table(
        'ai_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('prompt_length', sa.Integer(), nullable=True),
        sa.Column('response_length', sa.Integer(), nullable=True),
        sa.Column('input_tokens', sa.Integer(), nullable=True),
        sa.Column('output_tokens', sa.Integer(), nullable=True),
        sa.Column('total_tokens', sa.Integer(), nullable=True),
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('error_message', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_requests_organization_id'), 'ai_requests', ['organization_id'], unique=False)


def downgrade() -> None:
    op.drop_table('ai_requests')
    op.drop_table('ai_usage')
