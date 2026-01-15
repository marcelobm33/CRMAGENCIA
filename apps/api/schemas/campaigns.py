from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PlatformEnum(str, Enum):
    META = "meta"
    GOOGLE = "google"

class StatusEnum(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"

class CampaignBase(BaseModel):
    name: str
    platform: PlatformEnum
    status: StatusEnum = StatusEnum.ACTIVE
    external_id: str

class CampaignCreate(CampaignBase):
    pass

class CampaignMetrics(BaseModel):
    """Métricas calculadas da campanha"""
    impressions: int = 0
    clicks: int = 0
    spend: float = 0.0
    cpc: float = 0.0
    ctr: float = 0.0
    leads_generated: int = 0
    sales_closed: int = 0
    revenue: float = 0.0
    cpl: float = 0.0
    conversion_rate: float = 0.0
    roi: float = 0.0
    roas: float = 0.0

class Campaign(CampaignBase):
    id: int
    impressions: int
    clicks: int
    spend: float
    cpc: float
    ctr: float
    leads_generated: int
    sales_closed: int
    revenue: float
    cpl: float
    conversion_rate: float
    roi: float
    roas: float
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    last_sync: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CampaignSummary(BaseModel):
    """Resumo agregado de campanhas"""
    total_campaigns: int
    active_campaigns: int
    total_spend: float
    total_leads: int
    total_sales: int
    total_revenue: float
    avg_cpl: float
    avg_conversion_rate: float
    total_roi: float
    
class CampaignComparison(BaseModel):
    """Comparativo Meta vs Google"""
    meta: CampaignMetrics
    google: CampaignMetrics
    
class CampaignInsightResponse(BaseModel):
    date: datetime
    impressions: int
    clicks: int
    spend: float
    leads: int
    sales: int
    revenue: float
    
    class Config:
        from_attributes = True


# Aliases para compatibilidade
AdCampaignResponse = Campaign
AdSpendDailyResponse = CampaignInsightResponse


class AdPlatformAccountResponse(BaseModel):
    """Conta de plataforma de anúncios"""
    id: int
    platform: PlatformEnum
    account_id: str
    account_name: str
    is_active: bool = True
    last_sync: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
