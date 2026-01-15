"""
Script para popular o banco com dados de exemplo
Uso: python -m infra.seeds.run_seeds
"""
import asyncio
import random
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

from passlib.context import CryptContext

# Configurar path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'apps', 'api'))

from sqlalchemy import select
from database import async_session_maker, init_db
from models import User
from models.crm import CRMDeal, DealStatus
from models.campaigns import AdPlatformAccount, AdCampaign, AdSpendDaily, AdPlatform, CampaignStatus
from models.ai import AIRecommendation, RecommendationPriority, RecommendationScope, RecommendationStatus

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dados fake
VENDEDORES = [
    "Carlos Silva",
    "Maria Santos",
    "João Oliveira",
    "Ana Costa",
    "Pedro Souza"
]

ORIGENS = ["Site", "Telefone", "WhatsApp", "Indicação", "Feira", "Instagram", "Facebook"]

CANAIS = ["Google", "Meta", "Orgânico", "Direto", "Referral"]

VEICULOS = [
    "Honda Civic 2022", "Toyota Corolla 2023", "VW Golf 2021",
    "Hyundai HB20 2023", "Chevrolet Onix 2022", "Fiat Argo 2023",
    "Jeep Compass 2022", "Ford Ranger 2023", "Nissan Kicks 2022",
    "Renault Kwid 2023", "Peugeot 208 2022", "Citroën C3 2023"
]

MOTIVOS_PERDA = [
    "Preço alto",
    "Cliente não retornou",
    "Comprou em outro lugar",
    "Sem condições financeiras",
    "Desistiu da compra",
    "Veículo vendido",
    "Demora no atendimento"
]

CAMPANHAS_GOOGLE = [
    ("Busca - Carros Usados SP", "campaign_g1"),
    ("Busca - Seminovos Premium", "campaign_g2"),
    ("Display - Remarketing", "campaign_g3"),
    ("Busca - Financiamento", "campaign_g4"),
    ("Performance Max - Geral", "campaign_g5")
]

CAMPANHAS_META = [
    ("Leads - Ofertas Especiais", "campaign_m1"),
    ("Conversões - Catálogo", "campaign_m2"),
    ("Engajamento - Stories", "campaign_m3"),
    ("Remarketing - Visitantes", "campaign_m4"),
    ("Alcance - Branding", "campaign_m5")
]


async def create_admin_user(session):
    """Cria usuário admin padrão"""
    result = await session.execute(
        select(User).where(User.email == "admin@revenda.com")
    )
    if result.scalar_one_or_none():
        print("✓ Usuário admin já existe")
        return
    
    admin = User(
        email="admin@revenda.com",
        nome="Administrador",
        hashed_password=pwd_context.hash("admin123"),
        is_admin=True,
        is_active=True
    )
    session.add(admin)
    await session.commit()
    print("✓ Usuário admin criado (admin@revenda.com / admin123)")


async def create_deals(session, count=50):
    """Cria deals de exemplo"""
    print(f"Criando {count} deals de exemplo...")
    
    deals = []
    for i in range(count):
        # Data de criação nos últimos 60 dias
        days_ago = random.randint(0, 60)
        data_criacao = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))
        
        # Status com distribuição realista
        status_choice = random.random()
        if status_choice < 0.25:
            status = DealStatus.GANHO
            data_fechamento = data_criacao + timedelta(days=random.randint(1, 14))
            motivo = None
        elif status_choice < 0.70:
            status = DealStatus.PERDIDO
            data_fechamento = data_criacao + timedelta(days=random.randint(1, 7))
            motivo = random.choice(MOTIVOS_PERDA)
        else:
            status = DealStatus.ABERTO
            data_fechamento = None
            motivo = None
        
        # Valores
        valor = Decimal(str(random.randint(25000, 180000)))
        lucro = valor * Decimal(str(random.uniform(0.05, 0.15))) if status == DealStatus.GANHO else Decimal(0)
        
        # Canal e UTMs
        canal = random.choice(CANAIS)
        utm_source = None
        utm_campaign = None
        
        if canal == "Google":
            utm_source = "google"
            utm_campaign = random.choice(CAMPANHAS_GOOGLE)[0]
        elif canal == "Meta":
            utm_source = "facebook"
            utm_campaign = random.choice(CAMPANHAS_META)[0]
        
        deal = CRMDeal(
            data_criacao=data_criacao,
            data_fechamento=data_fechamento,
            status=status,
            motivo_perda=motivo,
            valor=valor,
            lucro_bruto=lucro.quantize(Decimal("0.01")),
            vendedor=random.choice(VENDEDORES),
            telefone=f"11 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            email=f"cliente{i}@email.com",
            nome_cliente=f"Cliente {i+1}",
            origem=random.choice(ORIGENS),
            canal=canal,
            utm_source=utm_source,
            utm_campaign=utm_campaign,
            veiculo_interesse=random.choice(VEICULOS),
            observacoes="Lead gerado automaticamente para testes" if random.random() > 0.7 else None
        )
        deals.append(deal)
    
    session.add_all(deals)
    await session.commit()
    print(f"✓ {count} deals criados")


async def create_campaigns_and_spend(session):
    """Cria campanhas e gastos de exemplo"""
    print("Criando campanhas e gastos...")
    
    # Criar contas
    google_account = AdPlatformAccount(
        platform=AdPlatform.GOOGLE,
        account_id="123-456-7890",
        account_name="Revenda Autos - Google Ads",
        is_active=True
    )
    meta_account = AdPlatformAccount(
        platform=AdPlatform.META,
        account_id="act_1234567890",
        account_name="Revenda Autos - Meta Ads",
        is_active=True
    )
    session.add_all([google_account, meta_account])
    await session.flush()
    
    # Criar campanhas Google
    google_campaigns = []
    for name, ext_id in CAMPANHAS_GOOGLE:
        campaign = AdCampaign(
            account_id=google_account.id,
            platform=AdPlatform.GOOGLE,
            campaign_id=ext_id,
            campaign_name=name,
            campaign_name_normalized=name.lower().replace(" ", "_"),
            status=CampaignStatus.ACTIVE,
            objective="LEADS"
        )
        google_campaigns.append(campaign)
    
    # Criar campanhas Meta
    meta_campaigns = []
    for name, ext_id in CAMPANHAS_META:
        campaign = AdCampaign(
            account_id=meta_account.id,
            platform=AdPlatform.META,
            campaign_id=ext_id,
            campaign_name=name,
            campaign_name_normalized=name.lower().replace(" ", "_"),
            status=CampaignStatus.ACTIVE,
            objective="LEAD_GENERATION"
        )
        meta_campaigns.append(campaign)
    
    session.add_all(google_campaigns + meta_campaigns)
    await session.flush()
    
    # Criar gastos diários (últimos 30 dias)
    spends = []
    all_campaigns = google_campaigns + meta_campaigns
    
    for day_offset in range(30):
        spend_date = (datetime.now() - timedelta(days=day_offset)).date()
        
        for campaign in all_campaigns:
            # Variação diária
            base_spend = random.uniform(50, 300)
            impressions = random.randint(1000, 10000)
            clicks = int(impressions * random.uniform(0.01, 0.05))
            leads = int(clicks * random.uniform(0.05, 0.20))
            
            spend = AdSpendDaily(
                date=spend_date,
                platform=campaign.platform,
                campaign_id_ref=campaign.id,
                campaign_external_id=campaign.campaign_id,
                spend=Decimal(str(round(base_spend, 2))),
                impressions=impressions,
                reach=int(impressions * 0.8),
                clicks=clicks,
                link_clicks=int(clicks * 0.9),
                leads=leads,
                conversions=leads,
                cpc=Decimal(str(round(base_spend / clicks, 4))) if clicks > 0 else Decimal(0),
                cpm=Decimal(str(round((base_spend / impressions) * 1000, 4))) if impressions > 0 else Decimal(0),
                ctr=Decimal(str(round((clicks / impressions) * 100, 4))) if impressions > 0 else Decimal(0),
                cpl=Decimal(str(round(base_spend / leads, 4))) if leads > 0 else Decimal(0)
            )
            spends.append(spend)
    
    session.add_all(spends)
    await session.commit()
    print(f"✓ {len(all_campaigns)} campanhas e {len(spends)} registros de gasto criados")


async def create_recommendations(session):
    """Cria recomendações de exemplo da IA"""
    print("Criando recomendações de exemplo...")
    
    recommendations = [
        AIRecommendation(
            escopo=RecommendationScope.CAMPANHA,
            prioridade=RecommendationPriority.HIGH,
            titulo="CPL elevado na campanha 'Busca - Financiamento'",
            insight="O CPL desta campanha está 40% acima da média das outras campanhas Google.",
            explicacao="Um CPL alto pode indicar problemas com a segmentação de palavras-chave ou com a página de destino. Leads caros impactam diretamente o ROI da campanha.",
            acoes_sugeridas=[
                {"acao": "Revisar termos de busca negativos", "tipo": "analise"},
                {"acao": "Testar nova landing page focada em financiamento", "tipo": "teste"},
                {"acao": "Reduzir lances em palavras com baixa conversão", "tipo": "otimizacao"}
            ],
            hipotese="Otimizando termos de busca, podemos reduzir CPL em 25%",
            metrica_alvo="CPL",
            impacto_esperado="Redução de R$ 20 no CPL médio",
            como_medir="Comparar CPL semanal antes e depois das mudanças",
            status=RecommendationStatus.PENDING
        ),
        AIRecommendation(
            escopo=RecommendationScope.ATENDIMENTO,
            prioridade=RecommendationPriority.CRITICAL,
            titulo="42% dos leads perdidos por 'cliente não retornou'",
            insight="Quase metade das perdas são por falta de retorno do cliente, indicando possível problema no follow-up.",
            explicacao="Quando o cliente não retorna, pode significar que o contato inicial demorou muito, que o follow-up não foi feito, ou que o interesse esfriou. Isso representa oportunidades perdidas.",
            acoes_sugeridas=[
                {"acao": "Implementar SLA de primeira resposta (máx 30 min)", "tipo": "imediata"},
                {"acao": "Criar sequência de follow-up automatizada", "tipo": "otimizacao"},
                {"acao": "Treinar equipe em técnicas de reativação", "tipo": "analise"}
            ],
            hipotese="Com SLA de atendimento, podemos recuperar 30% desses leads",
            metrica_alvo="Taxa de resposta",
            impacto_esperado="5-10 vendas adicionais por mês",
            como_medir="Monitorar tempo de primeira resposta e taxa de conversão",
            status=RecommendationStatus.IN_PROGRESS
        ),
        AIRecommendation(
            escopo=RecommendationScope.ORCAMENTO,
            prioridade=RecommendationPriority.MEDIUM,
            titulo="Oportunidade: campanha 'Leads - Ofertas Especiais' com excelente CPL",
            insight="Esta campanha Meta tem CPL 50% menor que a média e está gerando leads qualificados.",
            explicacao="Campanhas com boa performance são oportunidades de escala. Aumentar o orçamento pode trazer mais leads mantendo a qualidade.",
            acoes_sugeridas=[
                {"acao": "Aumentar orçamento diário em 30%", "tipo": "otimizacao"},
                {"acao": "Monitorar CPL após aumento", "tipo": "analise"}
            ],
            hipotese="Escalando a campanha, podemos manter CPL e aumentar volume",
            metrica_alvo="Volume de leads",
            impacto_esperado="15-20 leads adicionais por semana",
            como_medir="Acompanhar CPL e volume diário",
            status=RecommendationStatus.PENDING
        ),
        AIRecommendation(
            escopo=RecommendationScope.CRM,
            prioridade=RecommendationPriority.HIGH,
            titulo="Vendedor 'João Oliveira' com taxa de conversão abaixo da média",
            insight="João tem taxa de conversão de 15% vs média de 28% da equipe.",
            explicacao="Diferenças significativas entre vendedores podem indicar necessidade de treinamento ou problemas no processo de atribuição de leads.",
            acoes_sugeridas=[
                {"acao": "Acompanhar atendimentos do vendedor", "tipo": "analise"},
                {"acao": "Oferecer mentoria com vendedor top performer", "tipo": "otimizacao"},
                {"acao": "Revisar qualidade dos leads atribuídos", "tipo": "analise"}
            ],
            hipotese="Com treinamento, João pode atingir a média da equipe",
            metrica_alvo="Taxa de conversão por vendedor",
            impacto_esperado="3-5 vendas adicionais por mês",
            como_medir="Comparar taxa de conversão mensal",
            status=RecommendationStatus.PENDING
        ),
        AIRecommendation(
            escopo=RecommendationScope.CRIATIVO,
            prioridade=RecommendationPriority.LOW,
            titulo="Teste A/B sugerido: criativos de Stories",
            insight="Criativos de Stories no Meta têm CTR 2x maior que feed, mas volume menor.",
            explicacao="Formatos com alto engajamento merecem mais investimento e testes para maximizar resultados.",
            acoes_sugeridas=[
                {"acao": "Criar 3 novos criativos formato Stories", "tipo": "teste"},
                {"acao": "Testar diferentes CTAs", "tipo": "teste"}
            ],
            hipotese="Novos criativos podem aumentar CTR em 20%",
            metrica_alvo="CTR Stories",
            impacto_esperado="Mais cliques com mesmo investimento",
            como_medir="Comparar CTR antes e depois dos novos criativos",
            status=RecommendationStatus.DONE
        )
    ]
    
    session.add_all(recommendations)
    await session.commit()
    print(f"✓ {len(recommendations)} recomendações criadas")


async def main():
    """Executa todos os seeds"""
    print("\n" + "="*50)
    print("POPULANDO BANCO COM DADOS DE EXEMPLO")
    print("="*50 + "\n")
    
    async with async_session_maker() as session:
        await create_admin_user(session)
        await create_deals(session, count=50)
        await create_campaigns_and_spend(session)
        await create_recommendations(session)
    
    print("\n" + "="*50)
    print("✓ SEED CONCLUÍDO COM SUCESSO!")
    print("="*50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

