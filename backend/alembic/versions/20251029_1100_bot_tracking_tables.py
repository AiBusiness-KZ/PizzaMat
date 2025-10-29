"""Add bot interaction tracking tables

Revision ID: b1c2d3e4f5a6
Revises: f02f9c98a7a8
Create Date: 2025-10-29 11:00:00.000000+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b1c2d3e4f5a6'
down_revision = 'f02f9c98a7a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user_sessions table
    op.create_table(
        'user_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('telegram_id', sa.BigInteger(), nullable=False),
        sa.Column('session_start', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('session_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('language', sa.String(length=5), nullable=True),
        sa.Column('username', sa.String(length=255), nullable=True),
        sa.Column('first_name', sa.String(length=255), nullable=True),
        sa.Column('last_name', sa.String(length=255), nullable=True),
        sa.Column('messages_sent', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('commands_used', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('buttons_clicked', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('platform', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_sessions_id'), 'user_sessions', ['id'], unique=False)
    op.create_index(op.f('ix_user_sessions_user_id'), 'user_sessions', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_sessions_telegram_id'), 'user_sessions', ['telegram_id'], unique=False)
    op.create_index(op.f('ix_user_sessions_session_start'), 'user_sessions', ['session_start'], unique=False)

    # Create bot_interactions table
    op.create_table(
        'bot_interactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('telegram_id', sa.BigInteger(), nullable=False),
        sa.Column('interaction_type', sa.String(length=50), nullable=False),
        sa.Column('command', sa.String(length=100), nullable=True),
        sa.Column('message_text', sa.Text(), nullable=True),
        sa.Column('callback_data', sa.String(length=255), nullable=True),
        sa.Column('chat_id', sa.BigInteger(), nullable=False),
        sa.Column('message_id', sa.Integer(), nullable=True),
        sa.Column('bot_response', sa.Text(), nullable=True),
        sa.Column('bot_response_type', sa.String(length=50), nullable=True),
        sa.Column('fsm_state', sa.String(length=100), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_successful', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['user_sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bot_interactions_id'), 'bot_interactions', ['id'], unique=False)
    op.create_index(op.f('ix_bot_interactions_session_id'), 'bot_interactions', ['session_id'], unique=False)
    op.create_index(op.f('ix_bot_interactions_user_id'), 'bot_interactions', ['user_id'], unique=False)
    op.create_index(op.f('ix_bot_interactions_telegram_id'), 'bot_interactions', ['telegram_id'], unique=False)
    op.create_index(op.f('ix_bot_interactions_interaction_type'), 'bot_interactions', ['interaction_type'], unique=False)
    op.create_index(op.f('ix_bot_interactions_command'), 'bot_interactions', ['command'], unique=False)
    op.create_index(op.f('ix_bot_interactions_created_at'), 'bot_interactions', ['created_at'], unique=False)

    # Create support_messages table
    op.create_table(
        'support_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('telegram_id', sa.BigInteger(), nullable=False),
        sa.Column('ticket_id', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True, server_default='open'),
        sa.Column('sender_type', sa.String(length=20), nullable=False),
        sa.Column('sender_telegram_id', sa.BigInteger(), nullable=True),
        sa.Column('sender_name', sa.String(length=255), nullable=True),
        sa.Column('message_text', sa.Text(), nullable=False),
        sa.Column('message_type', sa.String(length=20), nullable=True, server_default='text'),
        sa.Column('file_url', sa.String(length=500), nullable=True),
        sa.Column('order_id', sa.Integer(), nullable=True),
        sa.Column('parent_message_id', sa.Integer(), nullable=True),
        sa.Column('thread_id', sa.String(length=20), nullable=True),
        sa.Column('responded_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('response_time_seconds', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.ForeignKeyConstraint(['parent_message_id'], ['support_messages.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ticket_id')
    )
    op.create_index(op.f('ix_support_messages_id'), 'support_messages', ['id'], unique=False)
    op.create_index(op.f('ix_support_messages_user_id'), 'support_messages', ['user_id'], unique=False)
    op.create_index(op.f('ix_support_messages_telegram_id'), 'support_messages', ['telegram_id'], unique=False)
    op.create_index(op.f('ix_support_messages_ticket_id'), 'support_messages', ['ticket_id'], unique=True)
    op.create_index(op.f('ix_support_messages_status'), 'support_messages', ['status'], unique=False)
    op.create_index(op.f('ix_support_messages_order_id'), 'support_messages', ['order_id'], unique=False)
    op.create_index(op.f('ix_support_messages_thread_id'), 'support_messages', ['thread_id'], unique=False)
    op.create_index(op.f('ix_support_messages_created_at'), 'support_messages', ['created_at'], unique=False)

    # Create bot_statistics table
    op.create_table(
        'bot_statistics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('total_users', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('new_users', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('active_users', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('total_sessions', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('avg_session_duration', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('total_interactions', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('total_commands', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('total_messages', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('total_callbacks', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('orders_created', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('orders_paid', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('orders_confirmed', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('orders_cancelled', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('orders_completed', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('total_revenue', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('avg_order_value', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('support_tickets_opened', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('support_tickets_closed', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('avg_response_time', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('menu_views', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('cart_additions', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('checkout_started', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('receipt_uploaded', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('top_commands', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('date')
    )
    op.create_index(op.f('ix_bot_statistics_id'), 'bot_statistics', ['id'], unique=False)
    op.create_index(op.f('ix_bot_statistics_date'), 'bot_statistics', ['date'], unique=True)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_bot_statistics_date'), table_name='bot_statistics')
    op.drop_index(op.f('ix_bot_statistics_id'), table_name='bot_statistics')
    op.drop_table('bot_statistics')

    op.drop_index(op.f('ix_support_messages_created_at'), table_name='support_messages')
    op.drop_index(op.f('ix_support_messages_thread_id'), table_name='support_messages')
    op.drop_index(op.f('ix_support_messages_order_id'), table_name='support_messages')
    op.drop_index(op.f('ix_support_messages_status'), table_name='support_messages')
    op.drop_index(op.f('ix_support_messages_ticket_id'), table_name='support_messages')
    op.drop_index(op.f('ix_support_messages_telegram_id'), table_name='support_messages')
    op.drop_index(op.f('ix_support_messages_user_id'), table_name='support_messages')
    op.drop_index(op.f('ix_support_messages_id'), table_name='support_messages')
    op.drop_table('support_messages')

    op.drop_index(op.f('ix_bot_interactions_created_at'), table_name='bot_interactions')
    op.drop_index(op.f('ix_bot_interactions_command'), table_name='bot_interactions')
    op.drop_index(op.f('ix_bot_interactions_interaction_type'), table_name='bot_interactions')
    op.drop_index(op.f('ix_bot_interactions_telegram_id'), table_name='bot_interactions')
    op.drop_index(op.f('ix_bot_interactions_user_id'), table_name='bot_interactions')
    op.drop_index(op.f('ix_bot_interactions_session_id'), table_name='bot_interactions')
    op.drop_index(op.f('ix_bot_interactions_id'), table_name='bot_interactions')
    op.drop_table('bot_interactions')

    op.drop_index(op.f('ix_user_sessions_session_start'), table_name='user_sessions')
    op.drop_index(op.f('ix_user_sessions_telegram_id'), table_name='user_sessions')
    op.drop_index(op.f('ix_user_sessions_user_id'), table_name='user_sessions')
    op.drop_index(op.f('ix_user_sessions_id'), table_name='user_sessions')
    op.drop_table('user_sessions')
