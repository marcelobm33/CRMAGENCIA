from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, Enum
from sqlalchemy.sql import func
from database import Base
import enum

class PlatformEnum(str, enum.Enum):
    META = "meta"
    GOOGLE = "google"
    
class StatusEnum(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"

class Campaign(Base):
    """
    Tabela para armazenar dados de campanhas (Meta + Google)
    Sincronizada via API a cada hora
    """
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Identificação
    external_id = Column(String(100), unique=True, index=True)  # ID da campanha na plataforma
    name = Column(String(255), nullable=False)
    platform = Column(Enum(PlatformEnum), nullable=False, index=True)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.ACTIVE)
    
    # Métricas da plataforma (Meta/Google Ads API)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    spend = Column(Float, default=0.0)  # Gasto em R$
    cpc = Column(Float, default=0.0)    # Custo por clique
    ctr = Column(Float, default=0.0)    # Click-through rate (%)
    
    # Métricas do CRM (calculadas do banco netcarrc01)
    leads_generated = Column(Integer, default=0)
    sales_closed = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    
    # Métricas calculadas
    cpl = Column(Float, default=0.0)    # Custo por lead
    conversion_rate = Column(Float, default=0.0)  # Taxa de conversão (%)
    roi = Column(Float, default=0.0)    # Return on Investment (%)
    roas = Column(Float, default=0.0)   # Return on Ad Spend
    
    # Período
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    
    # Metadados
    last_sync = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Dados adicionais (JSON)
    extra_data = Column(Text, nullable=True)  # JSON com dados extras da API


class CampaignInsight(Base):
    """
    Histórico diário de métricas de campanhas
    Para análise de tendências
    """
    __tablename__ = "campaign_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, index=True)
    external_campaign_id = Column(String(100), index=True)
    
    date = Column(DateTime, nullable=False, index=True)
    
    # Snapshot das métricas do dia
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    spend = Column(Float, default=0.0)
    leads = Column(Integer, default=0)
    sales = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=func.now())


class AdPlatformAccount(Base):
    """
    Contas de plataformas de anúncios conectadas
    """
    __tablename__ = "ad_platform_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(Enum(PlatformEnum), nullable=False)
    account_id = Column(String(100), nullable=False)
    account_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    last_sync = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


# Aliases para compatibilidade
AdSpendDaily = CampaignInsight
AdPlatform = PlatformEnum
AdCampaign = Campaign
