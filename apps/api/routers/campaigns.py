from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
from models.campaigns import Campaign, CampaignInsight
from schemas.campaigns import (
    Campaign as CampaignSchema,
    CampaignCreate,
    CampaignSummary,
    CampaignComparison,
    CampaignMetrics,
    PlatformEnum
)
from services.campaign_integrator import CampaignIntegrator
import os

router = APIRouter(prefix="/campaigns", tags=["Campanhas"])

# Conexão com CRM externo
def get_crm_db():
    """Retorna conexão com banco CRM (netcarrc01)"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    CRM_DATABASE_URL = f"mysql+pymysql://{os.getenv('CRM_DB_USER', 'netcarrc01_add1')}:{os.getenv('CRM_DB_PASS', 'netcar2025')}@{os.getenv('CRM_DB_HOST', 'mysql.netcar-rc.com.br')}/{os.getenv('CRM_DB_NAME', 'netcarrc01')}"
    
    engine = create_engine(CRM_DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[CampaignSchema])
def list_campaigns(
    platform: Optional[PlatformEnum] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todas as campanhas com filtros opcionais
    """
    query = db.query(Campaign)
    
    if platform:
        query = query.filter(Campaign.platform == platform)
    
    if status:
        query = query.filter(Campaign.status == status)
    
    campaigns = query.offset(skip).limit(limit).all()
    return campaigns


@router.get("/summary", response_model=CampaignSummary)
def get_campaigns_summary(
    days: int = Query(30, description="Últimos N dias"),
    db: Session = Depends(get_db),
    crm_db: Session = Depends(get_crm_db)
):
    """
    Retorna resumo geral de todas as campanhas
    """
    start_date = datetime.now() - timedelta(days=days)
    
    # Buscar todas as campanhas
    campaigns = db.query(Campaign).filter(
        Campaign.created_at >= start_date
    ).all()
    
    total_campaigns = len(campaigns)
    active_campaigns = len([c for c in campaigns if c.status == 'active'])
    
    total_spend = sum(c.spend for c in campaigns)
    total_leads = sum(c.leads_generated for c in campaigns)
    total_sales = sum(c.sales_closed for c in campaigns)
    total_revenue = sum(c.revenue for c in campaigns)
    
    avg_cpl = total_spend / total_leads if total_leads > 0 else 0
    avg_conversion_rate = (total_sales / total_leads * 100) if total_leads > 0 else 0
    total_roi = ((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0
    
    return {
        "total_campaigns": total_campaigns,
        "active_campaigns": active_campaigns,
        "total_spend": round(total_spend, 2),
        "total_leads": total_leads,
        "total_sales": total_sales,
        "total_revenue": round(total_revenue, 2),
        "avg_cpl": round(avg_cpl, 2),
        "avg_conversion_rate": round(avg_conversion_rate, 2),
        "total_roi": round(total_roi, 2)
    }


@router.get("/comparison", response_model=CampaignComparison)
def get_platform_comparison(
    days: int = Query(30, description="Últimos N dias"),
    db: Session = Depends(get_db),
    crm_db: Session = Depends(get_crm_db)
):
    """
    Comparativo META vs GOOGLE
    """
    start_date = datetime.now() - timedelta(days=days)
    end_date = datetime.now()
    
    integrator = CampaignIntegrator(db, crm_db)
    
    # Buscar campanhas por plataforma
    meta_campaigns = db.query(Campaign).filter(
        Campaign.platform == PlatformEnum.META,
        Campaign.created_at >= start_date
    ).all()
    
    google_campaigns = db.query(Campaign).filter(
        Campaign.platform == PlatformEnum.GOOGLE,
        Campaign.created_at >= start_date
    ).all()
    
    # Agregar métricas
    def aggregate_metrics(campaigns):
        return {
            "impressions": sum(c.impressions for c in campaigns),
            "clicks": sum(c.clicks for c in campaigns),
            "spend": sum(c.spend for c in campaigns),
            "cpc": sum(c.cpc for c in campaigns) / len(campaigns) if campaigns else 0,
            "ctr": sum(c.ctr for c in campaigns) / len(campaigns) if campaigns else 0,
            "leads_generated": sum(c.leads_generated for c in campaigns),
            "sales_closed": sum(c.sales_closed for c in campaigns),
            "revenue": sum(c.revenue for c in campaigns),
            "cpl": sum(c.cpl for c in campaigns) / len(campaigns) if campaigns else 0,
            "conversion_rate": sum(c.conversion_rate for c in campaigns) / len(campaigns) if campaigns else 0,
            "roi": sum(c.roi for c in campaigns) / len(campaigns) if campaigns else 0,
            "roas": sum(c.roas for c in campaigns) / len(campaigns) if campaigns else 0,
        }
    
    meta_metrics = aggregate_metrics(meta_campaigns)
    google_metrics = aggregate_metrics(google_campaigns)
    
    return {
        "meta": meta_metrics,
        "google": google_metrics
    }


@router.get("/top-performing")
def get_top_campaigns(
    limit: int = Query(5, description="Número de campanhas"),
    db: Session = Depends(get_db),
    crm_db: Session = Depends(get_crm_db)
):
    """
    Retorna as campanhas com melhor ROI
    """
    integrator = CampaignIntegrator(db, crm_db)
    return integrator.get_top_performing_campaigns(limit)


@router.get("/worst-performing")
def get_worst_campaigns(
    limit: int = Query(5, description="Número de campanhas"),
    db: Session = Depends(get_db),
    crm_db: Session = Depends(get_crm_db)
):
    """
    Retorna as campanhas que precisam de atenção (pior ROI)
    """
    integrator = CampaignIntegrator(db, crm_db)
    return integrator.get_worst_performing_campaigns(limit)


@router.get("/{campaign_id}")
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna detalhes de uma campanha específica
    """
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    
    return campaign


@router.post("/sync")
def sync_campaigns(
    db: Session = Depends(get_db),
    crm_db: Session = Depends(get_crm_db)
):
    """
    Sincroniza campanhas das APIs (Meta/Google) com dados do CRM
    Este endpoint deve ser chamado periodicamente (ex: a cada hora)
    """
    # TODO: Implementar sincronização real com APIs
    # Por enquanto, retorna status
    
    return {
        "status": "success",
        "message": "Sincronização iniciada. Conecte as APIs do Meta e Google para obter dados reais.",
        "timestamp": datetime.now()
    }
