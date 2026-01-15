"""
Tasks de sincronização com Google Ads
"""
import random
from datetime import datetime, timedelta, date
from decimal import Decimal
import structlog

from celery_app import app
from config import get_settings

logger = structlog.get_logger()
settings = get_settings()


@app.task(bind=True, max_retries=3)
def sync_google_ads(self):
    """
    Sincroniza dados do Google Ads
    
    Em modo mock: gera dados fake
    Em modo live: busca da API
    """
    logger.info("Iniciando sincronização Google Ads", mode="mock" if not settings.is_google_configured else "live")
    
    try:
        if settings.is_google_configured:
            # TODO: Implementar integração real com Google Ads API
            # from google.ads.googleads.client import GoogleAdsClient
            logger.info("Modo live - integração Google Ads não implementada ainda")
            return {"status": "skipped", "reason": "live integration not implemented"}
        
        # Modo mock - gerar dados fake
        today = date.today()
        campaigns_synced = generate_mock_google_data(today)
        
        logger.info("Sincronização Google Ads concluída", campaigns=campaigns_synced, mode="mock")
        return {"status": "success", "campaigns": campaigns_synced, "mode": "mock"}
        
    except Exception as e:
        logger.error("Erro na sincronização Google Ads", error=str(e))
        self.retry(exc=e, countdown=60 * (self.request.retries + 1))


@app.task(bind=True)
def reprocess_last_7_days(self):
    """
    Reprocessa os últimos 7 dias de dados
    Útil para corrigir dados que a plataforma pode ter atualizado
    """
    logger.info("Reprocessando últimos 7 dias")
    
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    # Em modo mock, apenas loga
    if not settings.is_google_configured:
        logger.info("Modo mock - reprocessamento simulado", start=str(start_date), end=str(end_date))
        return {"status": "success", "mode": "mock", "days": 7}
    
    # TODO: Implementar reprocessamento real
    return {"status": "skipped", "reason": "live integration not implemented"}


def generate_mock_google_data(target_date: date) -> int:
    """
    Gera dados mock para Google Ads
    Em produção, isso seria substituído pela chamada à API real
    """
    # Simula 5 campanhas
    campaigns = [
        "Busca - Carros Usados SP",
        "Busca - Seminovos Premium",
        "Display - Remarketing",
        "Busca - Financiamento",
        "Performance Max - Geral"
    ]
    
    for campaign in campaigns:
        # Dados mock com variação aleatória
        spend = Decimal(str(random.uniform(80, 250)))
        impressions = random.randint(2000, 8000)
        clicks = int(impressions * random.uniform(0.02, 0.06))
        leads = int(clicks * random.uniform(0.08, 0.18))
        
        logger.debug("Mock data gerado", 
            campaign=campaign,
            spend=float(spend),
            impressions=impressions,
            clicks=clicks,
            leads=leads
        )
    
    return len(campaigns)

