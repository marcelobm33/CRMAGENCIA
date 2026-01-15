"""
Serviço de integração entre APIs de anúncios (Meta/Google) e CRM
Sincroniza dados e calcula métricas combinadas
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)

class CampaignIntegrator:
    """
    Integra dados de campanhas (Meta/Google) com dados do CRM
    """
    
    def __init__(self, db: Session, crm_db: Session):
        self.db = db  # Banco local (campaigns)
        self.crm_db = crm_db  # Banco CRM (netcarrc01)
    
    def get_crm_leads_by_origin(self, origin: str, start_date: datetime, end_date: datetime) -> Dict:
        """
        Busca leads do CRM por origem (FACEBOOK, GOOGLE, etc)
        """
        query = """
        SELECT 
            COUNT(*) as total_leads,
            SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) as sales_closed,
            SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) as revenue,
            ROUND(
                SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) * 100.0 / 
                NULLIF(COUNT(*), 0), 
                2
            ) as conversion_rate
        FROM crm_negocio
        WHERE origem = :origin
          AND date_create BETWEEN :start_date AND :end_date
        """
        
        result = self.crm_db.execute(
            query,
            {
                "origin": origin,
                "start_date": start_date,
                "end_date": end_date
            }
        ).fetchone()
        
        return {
            "total_leads": result[0] or 0,
            "sales_closed": result[1] or 0,
            "revenue": float(result[2] or 0),
            "conversion_rate": float(result[3] or 0)
        }
    
    def calculate_campaign_metrics(self, campaign_data: Dict, crm_data: Dict) -> Dict:
        """
        Calcula métricas combinadas (API + CRM)
        """
        spend = campaign_data.get('spend', 0)
        impressions = campaign_data.get('impressions', 0)
        clicks = campaign_data.get('clicks', 0)
        
        leads = crm_data.get('total_leads', 0)
        sales = crm_data.get('sales_closed', 0)
        revenue = crm_data.get('revenue', 0)
        
        # Calcular métricas
        cpc = spend / clicks if clicks > 0 else 0
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpl = spend / leads if leads > 0 else 0
        conversion_rate = (sales / leads * 100) if leads > 0 else 0
        roi = ((revenue - spend) / spend * 100) if spend > 0 else 0
        roas = (revenue / spend) if spend > 0 else 0
        
        return {
            "impressions": impressions,
            "clicks": clicks,
            "spend": spend,
            "cpc": round(cpc, 2),
            "ctr": round(ctr, 2),
            "leads_generated": leads,
            "sales_closed": sales,
            "revenue": revenue,
            "cpl": round(cpl, 2),
            "conversion_rate": round(conversion_rate, 2),
            "roi": round(roi, 2),
            "roas": round(roas, 2)
        }
    
    def sync_meta_campaign(self, campaign_id: str, meta_data: Dict, start_date: datetime, end_date: datetime):
        """
        Sincroniza uma campanha do Meta Ads com dados do CRM
        """
        # Mapear origem do CRM
        origin_mapping = {
            "meta": "FACEBOOK",  # Pode ser FACEBOOK ou INSTAGRAM
            "facebook": "FACEBOOK",
            "instagram": "INSTAGRAM"
        }
        
        crm_origin = origin_mapping.get(meta_data.get('platform', 'meta').lower(), 'FACEBOOK')
        
        # Buscar dados do CRM
        crm_data = self.get_crm_leads_by_origin(crm_origin, start_date, end_date)
        
        # Calcular métricas combinadas
        metrics = self.calculate_campaign_metrics(meta_data, crm_data)
        
        return metrics
    
    def sync_google_campaign(self, campaign_id: str, google_data: Dict, start_date: datetime, end_date: datetime):
        """
        Sincroniza uma campanha do Google Ads com dados do CRM
        """
        # Buscar dados do CRM (origem = GOOGLE)
        crm_data = self.get_crm_leads_by_origin('GOOGLE', start_date, end_date)
        
        # Calcular métricas combinadas
        metrics = self.calculate_campaign_metrics(google_data, crm_data)
        
        return metrics
    
    def get_campaign_comparison(self, start_date: datetime, end_date: datetime) -> Dict:
        """
        Retorna comparativo META vs GOOGLE
        """
        # Dados agregados do Meta
        meta_origins = ['FACEBOOK', 'INSTAGRAM']
        meta_data = {
            'total_leads': 0,
            'sales_closed': 0,
            'revenue': 0
        }
        
        for origin in meta_origins:
            data = self.get_crm_leads_by_origin(origin, start_date, end_date)
            meta_data['total_leads'] += data['total_leads']
            meta_data['sales_closed'] += data['sales_closed']
            meta_data['revenue'] += data['revenue']
        
        # Dados do Google
        google_data = self.get_crm_leads_by_origin('GOOGLE', start_date, end_date)
        
        return {
            "meta": meta_data,
            "google": google_data
        }
    
    def get_top_performing_campaigns(self, limit: int = 5) -> List[Dict]:
        """
        Retorna as campanhas com melhor ROI
        """
        query = """
        SELECT 
            id,
            name,
            platform,
            spend,
            leads_generated,
            sales_closed,
            revenue,
            roi,
            roas
        FROM campaigns
        WHERE status = 'active'
        ORDER BY roi DESC
        LIMIT :limit
        """
        
        results = self.db.execute(query, {"limit": limit}).fetchall()
        
        return [
            {
                "id": r[0],
                "name": r[1],
                "platform": r[2],
                "spend": r[3],
                "leads": r[4],
                "sales": r[5],
                "revenue": r[6],
                "roi": r[7],
                "roas": r[8]
            }
            for r in results
        ]
    
    def get_worst_performing_campaigns(self, limit: int = 5) -> List[Dict]:
        """
        Retorna as campanhas com pior ROI (precisam de atenção)
        """
        query = """
        SELECT 
            id,
            name,
            platform,
            spend,
            leads_generated,
            sales_closed,
            revenue,
            roi,
            cpl
        FROM campaigns
        WHERE status = 'active'
        ORDER BY roi ASC
        LIMIT :limit
        """
        
        results = self.db.execute(query, {"limit": limit}).fetchall()
        
        return [
            {
                "id": r[0],
                "name": r[1],
                "platform": r[2],
                "spend": r[3],
                "leads": r[4],
                "sales": r[5],
                "revenue": r[6],
                "roi": r[7],
                "cpl": r[8]
            }
            for r in results
        ]

