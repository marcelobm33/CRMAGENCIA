"""
Schemas Pydantic para dados da agência
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field


class AgencyReportBase(BaseModel):
    """Base para relatório da agência"""
    ano: int
    mes: int
    
    # Investimentos
    investimento_meta: Decimal = 0
    investimento_google: Decimal = 0
    investimento_tiktok: Decimal = 0
    investimento_outros: Decimal = 0
    
    # META
    meta_alcance: int = 0
    meta_impressoes: int = 0
    meta_cliques: int = 0
    meta_conversoes: int = 0
    meta_visitas_perfil: int = 0
    
    # GOOGLE
    google_impressoes: int = 0
    google_cliques: int = 0
    google_conversoes: int = 0
    google_chamadas: int = 0
    google_whatsapp: int = 0
    google_visitas_loja: int = 0
    google_custo_conversao: Decimal = 0
    
    # TikTok
    tiktok_visualizacoes: int = 0
    tiktok_seguidores: int = 0
    
    # Instagram
    instagram_novos_seguidores: int = 0
    instagram_publicacoes: int = 0
    instagram_stories: int = 0
    instagram_likes: int = 0
    
    # Totais
    total_leads_reportados: int = 0
    total_vendas_reportadas: int = 0
    
    observacoes: Optional[str] = None


class AgencyReportCreate(AgencyReportBase):
    """Para criar novo relatório"""
    pass


class AgencyReportResponse(AgencyReportBase):
    """Resposta com relatório"""
    id: int
    investimento_total: Decimal
    created_at: datetime
    
    class Config:
        from_attributes = True


class ROIAnalysisResponse(BaseModel):
    """Resposta com análise de ROI"""
    ano: int
    mes: int
    periodo: str
    
    # CRM (Realidade)
    crm: dict
    
    # Agência
    agencia: dict
    
    # ROI Calculado
    roi: dict
    
    # Comparativo
    comparativo: dict
    
    # Insights
    insights: List[str]


class DashboardCruzamentoResponse(BaseModel):
    """Resposta do dashboard de cruzamento"""
    periodo: str
    
    # Resumo
    investimento_total: Decimal
    leads_agencia: int
    leads_crm: int
    vendas_crm: int
    valor_vendido: Decimal
    
    # ROI
    custo_por_lead_agencia: Decimal
    custo_por_lead_real: Decimal
    custo_por_venda: Decimal
    roi_percentual: Decimal
    
    # Por Canal
    meta: dict
    google: dict
    
    # Funil
    funil: dict
    
    # Alertas
    alertas: List[str]
    
    # Insights
    insights: List[str]
