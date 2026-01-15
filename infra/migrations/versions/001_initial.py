"""Initial migration - Create all tables

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_admin', sa.Boolean(), nullable=False, default=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # CRM Deals table
    op.create_table('crm_deals',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('data_criacao', sa.DateTime(timezone=True), nullable=False),
        sa.Column('data_fechamento', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.Enum('aberto', 'ganho', 'perdido', name='dealstatus'), nullable=False),
        sa.Column('motivo_perda', sa.String(length=255), nullable=True),
        sa.Column('valor', sa.Numeric(precision=15, scale=2), nullable=False, default=0),
        sa.Column('lucro_bruto', sa.Numeric(precision=15, scale=2), nullable=False, default=0),
        sa.Column('vendedor', sa.String(length=255), nullable=False),
        sa.Column('telefone', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('nome_cliente', sa.String(length=255), nullable=True),
        sa.Column('origem', sa.String(length=100), nullable=True),
        sa.Column('canal', sa.String(length=100), nullable=True),
        sa.Column('utm_source', sa.String(length=255), nullable=True),
        sa.Column('utm_medium', sa.String(length=255), nullable=True),
        sa.Column('utm_campaign', sa.String(length=255), nullable=True),
        sa.Column('utm_content', sa.String(length=255), nullable=True),
        sa.Column('utm_term', sa.String(length=255), nullable=True),
        sa.Column('gclid', sa.String(length=255), nullable=True),
        sa.Column('fbclid', sa.String(length=255), nullable=True),
        sa.Column('veiculo_interesse', sa.String(length=255), nullable=True),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_crm_deals_vendedor', 'crm_deals', ['vendedor'])
    op.create_index('ix_crm_deals_status', 'crm_deals', ['status'])
    op.create_index('ix_crm_deals_data_criacao', 'crm_deals', ['data_criacao'])

    # Ad Platform Accounts table
    op.create_table('ad_platform_accounts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('platform', sa.Enum('google', 'meta', name='adplatform'), nullable=False),
        sa.Column('account_id', sa.String(length=100), nullable=False),
        sa.Column('account_name', sa.String(length=255), nullable=False),
        sa.Column('credentials_encrypted', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('last_synced', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('account_id')
    )

    # Ad Campaigns table
    op.create_table('ad_campaigns',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('account_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('platform', sa.Enum('google', 'meta', name='adplatform', create_type=False), nullable=False),
        sa.Column('campaign_id', sa.String(length=100), nullable=False),
        sa.Column('campaign_name', sa.String(length=500), nullable=False),
        sa.Column('campaign_name_normalized', sa.String(length=500), nullable=True),
        sa.Column('status', sa.Enum('active', 'paused', 'removed', 'unknown', name='campaignstatus'), nullable=False),
        sa.Column('objective', sa.String(length=100), nullable=True),
        sa.Column('last_synced', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['account_id'], ['ad_platform_accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ad_campaigns_platform', 'ad_campaigns', ['platform'])
    op.create_index('ix_ad_campaigns_campaign_id', 'ad_campaigns', ['campaign_id'])

    # Ad Spend Daily table
    op.create_table('ad_spend_daily',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('platform', sa.Enum('google', 'meta', name='adplatform', create_type=False), nullable=False),
        sa.Column('campaign_id_ref', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('campaign_external_id', sa.String(length=100), nullable=False),
        sa.Column('adset_id', sa.String(length=100), nullable=True),
        sa.Column('adset_name', sa.String(length=500), nullable=True),
        sa.Column('ad_id', sa.String(length=100), nullable=True),
        sa.Column('ad_name', sa.String(length=500), nullable=True),
        sa.Column('spend', sa.Numeric(precision=15, scale=2), nullable=False, default=0),
        sa.Column('impressions', sa.Integer(), nullable=False, default=0),
        sa.Column('reach', sa.Integer(), nullable=False, default=0),
        sa.Column('clicks', sa.Integer(), nullable=False, default=0),
        sa.Column('link_clicks', sa.Integer(), nullable=False, default=0),
        sa.Column('leads', sa.Integer(), nullable=False, default=0),
        sa.Column('conversions', sa.Integer(), nullable=False, default=0),
        sa.Column('cpc', sa.Numeric(precision=10, scale=4), nullable=False, default=0),
        sa.Column('cpm', sa.Numeric(precision=10, scale=4), nullable=False, default=0),
        sa.Column('ctr', sa.Numeric(precision=10, scale=4), nullable=False, default=0),
        sa.Column('cpl', sa.Numeric(precision=10, scale=4), nullable=False, default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id_ref'], ['ad_campaigns.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ad_spend_daily_date', 'ad_spend_daily', ['date'])
    op.create_index('ix_ad_spend_daily_platform', 'ad_spend_daily', ['platform'])

    # Attribution Links table
    op.create_table('attribution_links',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('deal_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('campaign_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('method', sa.Enum('utm', 'gclid', 'fbclid', 'manual', 'rule', 'ai', name='attributionmethod'), nullable=False),
        sa.Column('confidence', sa.Numeric(precision=5, scale=4), nullable=False, default=1.0),
        sa.Column('match_details', sa.String(length=500), nullable=True),
        sa.Column('created_by', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['deal_id'], ['crm_deals.id'], ),
        sa.ForeignKeyConstraint(['campaign_id'], ['ad_campaigns.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # KPI Snapshots table
    op.create_table('kpi_snapshots',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('periodo_inicio', sa.Date(), nullable=False),
        sa.Column('periodo_fim', sa.Date(), nullable=False),
        sa.Column('agregacao', sa.Enum('daily', 'weekly', 'monthly', 'custom', name='aggregationtype'), nullable=False),
        sa.Column('canal', sa.String(length=100), nullable=True),
        sa.Column('campaign_id', sa.String(length=100), nullable=True),
        sa.Column('vendedor', sa.String(length=255), nullable=True),
        sa.Column('metricas', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # AI Recommendations table
    op.create_table('ai_recommendations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('data', sa.DateTime(timezone=True), nullable=False),
        sa.Column('escopo', sa.Enum('campanha', 'criativo', 'publico', 'orcamento', 'landing', 'atendimento', 'followup', 'crm', 'geral', name='recommendationscope'), nullable=False),
        sa.Column('prioridade', sa.Enum('critical', 'high', 'medium', 'low', name='recommendationpriority'), nullable=False),
        sa.Column('titulo', sa.String(length=500), nullable=False),
        sa.Column('insight', sa.Text(), nullable=False),
        sa.Column('explicacao', sa.Text(), nullable=False),
        sa.Column('acoes_sugeridas', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('hipotese', sa.Text(), nullable=True),
        sa.Column('metrica_alvo', sa.String(length=100), nullable=True),
        sa.Column('impacto_esperado', sa.Text(), nullable=True),
        sa.Column('como_medir', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('pending', 'in_progress', 'done', 'dismissed', 'testing', name='recommendationstatus'), nullable=False),
        sa.Column('contexto_dados', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('notas_usuario', sa.Text(), nullable=True),
        sa.Column('resultado_obtido', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ai_recommendations_status', 'ai_recommendations', ['status'])
    op.create_index('ix_ai_recommendations_prioridade', 'ai_recommendations', ['prioridade'])


def downgrade() -> None:
    op.drop_table('ai_recommendations')
    op.drop_table('kpi_snapshots')
    op.drop_table('attribution_links')
    op.drop_table('ad_spend_daily')
    op.drop_table('ad_campaigns')
    op.drop_table('ad_platform_accounts')
    op.drop_table('crm_deals')
    op.drop_table('users')
    
    # Drop enums
    op.execute("DROP TYPE IF EXISTS recommendationstatus")
    op.execute("DROP TYPE IF EXISTS recommendationpriority")
    op.execute("DROP TYPE IF EXISTS recommendationscope")
    op.execute("DROP TYPE IF EXISTS aggregationtype")
    op.execute("DROP TYPE IF EXISTS attributionmethod")
    op.execute("DROP TYPE IF EXISTS campaignstatus")
    op.execute("DROP TYPE IF EXISTS adplatform")
    op.execute("DROP TYPE IF EXISTS dealstatus")

