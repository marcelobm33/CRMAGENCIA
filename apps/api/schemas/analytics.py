"""
Schemas para analytics e KPIs
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Dict
from uuid import UUID
from pydantic import BaseModel


class KPISnapshotResponse(BaseModel):
    """Schema de resposta para snapshot de KPI"""
    id: UUID
    periodo_inicio: date
    periodo_fim: date
    agregacao: str
    canal: Optional[str]
    campaign_id: Optional[str]
    vendedor: Optional[str]
    metricas: dict
    created_at: datetime
    
    class Config:
        from_attributes = True


class MetricCard(BaseModel):
    """Card de métrica para dashboard"""
    label: str
    valor: str
    variacao: Optional[float] = None  # % de variação vs período anterior
    variacao_positiva: Optional[bool] = None


class DashboardOverview(BaseModel):
    """Visão geral do dashboard"""
    periodo_inicio: date
    periodo_fim: date
    
    # Cards principais
    gasto_total: MetricCard
    leads_total: MetricCard
    deals_total: MetricCard
    deals_ganhos: MetricCard
    taxa_conversao: MetricCard
    cpl: MetricCard
    cpa: MetricCard
    receita_total: MetricCard
    lucro_bruto: MetricCard
    roas: MetricCard
    
    # Série temporal (para gráficos)
    serie_diaria: List[Dict]


class ChannelMetrics(BaseModel):
    """Métricas por canal (Google vs Meta)"""
    canal: str
    gasto: Decimal
    impressoes: int
    cliques: int
    leads: int
    deals: int
    deals_ganhos: int
    taxa_conversao: float
    cpl: Decimal
    cpa: Decimal
    receita: Decimal
    roas: Optional[Decimal]


class ChannelComparisonResponse(BaseModel):
    """Comparação entre canais"""
    periodo_inicio: date
    periodo_fim: date
    canais: List[ChannelMetrics]


class VendedorMetrics(BaseModel):
    """Métricas por vendedor"""
    vendedor: str
    deals_total: int
    deals_ganhos: int
    deals_perdidos: int
    deals_abertos: int
    taxa_conversao: float
    valor_total: Decimal
    lucro_bruto: Decimal
    ticket_medio: Decimal
    tempo_medio_fechamento: Optional[int]  # em dias


class VendedorListResponse(BaseModel):
    """Lista de vendedores com métricas"""
    periodo_inicio: date
    periodo_fim: date
    vendedores: List[VendedorMetrics]


class MotivoPerdaItem(BaseModel):
    """Item de motivo de perda"""
    motivo: str
    quantidade: int
    percentual: float


class FunnelMetrics(BaseModel):
    """Métricas do funil de vendas"""
    periodo_inicio: date
    periodo_fim: date
    
    # Totais
    total_leads: int
    total_deals: int
    deals_abertos: int
    deals_ganhos: int
    deals_perdidos: int
    
    # Taxas
    taxa_lead_to_deal: float
    taxa_conversao: float
    taxa_perda: float
    
    # Motivos de perda
    motivos_perda: List[MotivoPerdaItem]
    
    # Série temporal
    serie_diaria: List[Dict]

