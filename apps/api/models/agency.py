"""
Modelos para dados da agência de marketing (Voren)
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class AgencyMonthlyReport(Base):
    """
    Relatório mensal da agência de marketing
    Armazena os dados consolidados que a agência reporta
    """
    __tablename__ = "agency_monthly_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Período
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    
    # Investimentos
    investimento_meta = Column(Numeric(12, 2), default=0)
    investimento_google = Column(Numeric(12, 2), default=0)
    investimento_tiktok = Column(Numeric(12, 2), default=0)
    investimento_outros = Column(Numeric(12, 2), default=0)
    investimento_total = Column(Numeric(12, 2), default=0)
    
    # Métricas META
    meta_alcance = Column(Integer, default=0)
    meta_impressoes = Column(Integer, default=0)
    meta_cliques = Column(Integer, default=0)
    meta_conversoes = Column(Integer, default=0)  # Leads reportados
    meta_visitas_perfil = Column(Integer, default=0)
    meta_engajamento = Column(Integer, default=0)
    
    # Métricas GOOGLE
    google_impressoes = Column(Integer, default=0)
    google_cliques = Column(Integer, default=0)
    google_conversoes = Column(Integer, default=0)  # Leads reportados
    google_chamadas = Column(Integer, default=0)
    google_whatsapp = Column(Integer, default=0)
    google_visitas_loja = Column(Integer, default=0)
    google_custo_conversao = Column(Numeric(10, 2), default=0)
    
    # Métricas TikTok
    tiktok_visualizacoes = Column(Integer, default=0)
    tiktok_seguidores = Column(Integer, default=0)
    tiktok_curtidas = Column(Integer, default=0)
    
    # Instagram
    instagram_novos_seguidores = Column(Integer, default=0)
    instagram_publicacoes = Column(Integer, default=0)
    instagram_stories = Column(Integer, default=0)
    instagram_likes = Column(Integer, default=0)
    instagram_comentarios = Column(Integer, default=0)
    instagram_compartilhamentos = Column(Integer, default=0)
    
    # Totais reportados pela agência
    total_leads_reportados = Column(Integer, default=0)
    total_vendas_reportadas = Column(Integer, default=0)
    
    # Observações
    observacoes = Column(Text, nullable=True)
    arquivo_pdf = Column(String(255), nullable=True)
    
    # Controle
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<AgencyReport {self.ano}-{self.mes:02d}>"


class AgencyCampaignDetail(Base):
    """
    Detalhes por campanha específica (opcional, para análise granular)
    """
    __tablename__ = "agency_campaign_details"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("agency_monthly_reports.id"), nullable=False)
    
    plataforma = Column(String(50), nullable=False)  # META, GOOGLE, TIKTOK
    nome_campanha = Column(String(255), nullable=False)
    objetivo = Column(String(100), nullable=True)  # vendas_whatsapp, vendas_site, alcance, etc.
    
    investimento = Column(Numeric(10, 2), default=0)
    impressoes = Column(Integer, default=0)
    cliques = Column(Integer, default=0)
    conversoes = Column(Integer, default=0)
    custo_conversao = Column(Numeric(10, 2), default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento
    report = relationship("AgencyMonthlyReport", backref="campaigns")


class ROIAnalysis(Base):
    """
    Análise de ROI calculada automaticamente (CRM vs Agência)
    """
    __tablename__ = "roi_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Período
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    
    # Dados do CRM (realidade)
    crm_leads_total = Column(Integer, default=0)
    crm_leads_meta = Column(Integer, default=0)
    crm_leads_google = Column(Integer, default=0)
    crm_leads_outros = Column(Integer, default=0)
    
    crm_vendas_total = Column(Integer, default=0)
    crm_vendas_meta = Column(Integer, default=0)
    crm_vendas_google = Column(Integer, default=0)
    crm_vendas_outros = Column(Integer, default=0)
    
    crm_valor_vendido_total = Column(Numeric(14, 2), default=0)
    crm_valor_vendido_meta = Column(Numeric(14, 2), default=0)
    crm_valor_vendido_google = Column(Numeric(14, 2), default=0)
    crm_valor_vendido_outros = Column(Numeric(14, 2), default=0)
    
    # Dados da agência
    agencia_investimento_total = Column(Numeric(12, 2), default=0)
    agencia_investimento_meta = Column(Numeric(12, 2), default=0)
    agencia_investimento_google = Column(Numeric(12, 2), default=0)
    agencia_leads_reportados = Column(Integer, default=0)
    
    # Cálculos de ROI
    custo_por_lead_real = Column(Numeric(10, 2), default=0)
    custo_por_venda_real = Column(Numeric(10, 2), default=0)
    roi_total = Column(Numeric(10, 2), default=0)  # (Valor Vendido / Investimento) * 100
    
    custo_por_lead_meta = Column(Numeric(10, 2), default=0)
    custo_por_venda_meta = Column(Numeric(10, 2), default=0)
    roi_meta = Column(Numeric(10, 2), default=0)
    
    custo_por_lead_google = Column(Numeric(10, 2), default=0)
    custo_por_venda_google = Column(Numeric(10, 2), default=0)
    roi_google = Column(Numeric(10, 2), default=0)
    
    # Discrepâncias
    diferenca_leads = Column(Integer, default=0)  # CRM - Agência
    taxa_conversao_real = Column(Numeric(5, 2), default=0)  # Vendas / Leads CRM
    
    # Insights gerados
    insights = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
