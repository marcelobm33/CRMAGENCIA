"""
Seed de dados de exemplo para campanhas
Simula dados reais de Meta Ads e Google Ads
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.campaigns import Campaign, Base
import random

# Configuração do banco
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crm_ia.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Criar tabelas
Base.metadata.create_all(bind=engine)

def create_sample_campaigns():
    """Cria campanhas de exemplo com dados realistas"""
    db = SessionLocal()
    
    # Limpar dados existentes
    db.query(Campaign).delete()
    
    campaigns_data = [
        # META CAMPAIGNS
        {
            "external_id": "meta_001",
            "name": "Busca - Seminovos Premium",
            "platform": "meta",
            "status": "active",
            "impressions": 50000,
            "clicks": 380,
            "spend": 1250.00,
            "leads_generated": 45,
            "sales_closed": 12,
            "revenue": 145000.00,
            "start_date": datetime.now() - timedelta(days=30)
        },
        {
            "external_id": "meta_002",
            "name": "Leads - Ofertas Especiais",
            "platform": "meta",
            "status": "active",
            "impressions": 75000,
            "clicks": 520,
            "spend": 980.00,
            "leads_generated": 38,
            "sales_closed": 10,
            "revenue": 118000.00,
            "start_date": datetime.now() - timedelta(days=25)
        },
        {
            "external_id": "meta_003",
            "name": "Busca - Carros Usados SP",
            "platform": "meta",
            "status": "active",
            "impressions": 42000,
            "clicks": 285,
            "spend": 1532.00,
            "leads_generated": 32,
            "sales_closed": 5,
            "revenue": 62000.00,
            "start_date": datetime.now() - timedelta(days=20)
        },
        {
            "external_id": "meta_004",
            "name": "Remarketing - Visitantes",
            "platform": "meta",
            "status": "active",
            "impressions": 28000,
            "clicks": 420,
            "spend": 655.00,
            "leads_generated": 28,
            "sales_closed": 4,
            "revenue": 48000.00,
            "start_date": datetime.now() - timedelta(days=15)
        },
        {
            "external_id": "meta_005",
            "name": "Display - Remarketing",
            "platform": "meta",
            "status": "paused",
            "impressions": 95000,
            "clicks": 180,
            "spend": 420.00,
            "leads_generated": 8,
            "sales_closed": 1,
            "revenue": 12000.00,
            "start_date": datetime.now() - timedelta(days=10)
        },
        {
            "external_id": "meta_006",
            "name": "Busca - Financiamento",
            "platform": "meta",
            "status": "active",
            "impressions": 38000,
            "clicks": 245,
            "spend": 1331.50,
            "leads_generated": 13,
            "sales_closed": 0,
            "revenue": 0.00,
            "start_date": datetime.now() - timedelta(days=5)
        },
        
        # GOOGLE CAMPAIGNS
        {
            "external_id": "google_001",
            "name": "Busca - Seminovos Premium",
            "platform": "google",
            "status": "active",
            "impressions": 65000,
            "clicks": 520,
            "spend": 1250.00,
            "leads_generated": 45,
            "sales_closed": 12,
            "revenue": 145000.00,
            "start_date": datetime.now() - timedelta(days=30)
        },
        {
            "external_id": "google_002",
            "name": "Leads - Ofertas Especiais",
            "platform": "google",
            "status": "active",
            "impressions": 48000,
            "clicks": 380,
            "spend": 980.00,
            "leads_generated": 38,
            "sales_closed": 10,
            "revenue": 118000.00,
            "start_date": datetime.now() - timedelta(days=25)
        },
        {
            "external_id": "google_003",
            "name": "Busca - Carros Usados SP",
            "platform": "google",
            "status": "active",
            "impressions": 55000,
            "clicks": 425,
            "spend": 1532.00,
            "leads_generated": 32,
            "sales_closed": 5,
            "revenue": 62000.00,
            "start_date": datetime.now() - timedelta(days=20)
        },
        {
            "external_id": "google_004",
            "name": "Remarketing - Visitantes",
            "platform": "google",
            "status": "active",
            "impressions": 32000,
            "clicks": 285,
            "spend": 655.00,
            "leads_generated": 28,
            "sales_closed": 4,
            "revenue": 48000.00,
            "start_date": datetime.now() - timedelta(days=15)
        },
        {
            "external_id": "google_005",
            "name": "Display - Remarketing",
            "platform": "google",
            "status": "active",
            "impressions": 78000,
            "clicks": 195,
            "spend": 420.00,
            "leads_generated": 8,
            "sales_closed": 1,
            "revenue": 12000.00,
            "start_date": datetime.now() - timedelta(days=10)
        }
    ]
    
    for data in campaigns_data:
        # Calcular métricas
        impressions = data['impressions']
        clicks = data['clicks']
        spend = data['spend']
        leads = data['leads_generated']
        sales = data['sales_closed']
        revenue = data['revenue']
        
        cpc = spend / clicks if clicks > 0 else 0
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpl = spend / leads if leads > 0 else 0
        conversion_rate = (sales / leads * 100) if leads > 0 else 0
        roi = ((revenue - spend) / spend * 100) if spend > 0 else 0
        roas = (revenue / spend) if spend > 0 else 0
        
        campaign = Campaign(
            external_id=data['external_id'],
            name=data['name'],
            platform=data['platform'],
            status=data['status'],
            impressions=impressions,
            clicks=clicks,
            spend=spend,
            cpc=round(cpc, 2),
            ctr=round(ctr, 2),
            leads_generated=leads,
            sales_closed=sales,
            revenue=revenue,
            cpl=round(cpl, 2),
            conversion_rate=round(conversion_rate, 2),
            roi=round(roi, 2),
            roas=round(roas, 2),
            start_date=data['start_date'],
            last_sync=datetime.now()
        )
        
        db.add(campaign)
    
    db.commit()
    print(f"✅ {len(campaigns_data)} campanhas criadas com sucesso!")
    
    # Mostrar resumo
    meta_count = len([c for c in campaigns_data if c['platform'] == 'meta'])
    google_count = len([c for c in campaigns_data if c['platform'] == 'google'])
    
    print(f"\n📊 Resumo:")
    print(f"   • Meta Ads: {meta_count} campanhas")
    print(f"   • Google Ads: {google_count} campanhas")
    
    db.close()

if __name__ == "__main__":
    print("🌱 Criando dados de exemplo para campanhas...")
    create_sample_campaigns()
    print("\n✨ Pronto! Acesse http://localhost:8000/api/campaigns para ver as campanhas.")

