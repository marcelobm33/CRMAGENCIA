"""
Router de Analytics e KPIs
"""
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import User
from models.crm import CRMDeal, DealStatus
from models.campaigns import AdSpendDaily, AdPlatform
from schemas.analytics import (
    DashboardOverview,
    MetricCard,
    ChannelMetrics,
    ChannelComparisonResponse,
    VendedorMetrics,
    VendedorListResponse,
    FunnelMetrics,
    MotivoPerdaItem
)
from routers.auth import get_current_user

router = APIRouter()


def format_currency(value: float) -> str:
    """Formata valor como moeda BRL"""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_number(value: int) -> str:
    """Formata número com separador de milhar"""
    return f"{value:,}".replace(",", ".")


def format_percent(value: float) -> str:
    """Formata percentual"""
    return f"{value:.1f}%"


@router.get("/overview", response_model=DashboardOverview)
async def get_dashboard_overview(
    dias: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Visão geral do dashboard com métricas principais
    """
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias)
    
    # Período anterior para comparação
    data_inicio_anterior = data_inicio - timedelta(days=dias)
    data_fim_anterior = data_inicio - timedelta(days=1)
    
    # --- Métricas de Gastos ---
    spend_query = select(
        func.sum(AdSpendDaily.spend),
        func.sum(AdSpendDaily.leads)
    ).where(
        AdSpendDaily.date >= data_inicio,
        AdSpendDaily.date <= data_fim
    )
    spend_result = await db.execute(spend_query)
    spend_row = spend_result.one()
    gasto_total = float(spend_row[0] or 0)
    leads_total = spend_row[1] or 0
    
    # Período anterior
    spend_anterior = await db.execute(
        select(func.sum(AdSpendDaily.spend), func.sum(AdSpendDaily.leads))
        .where(AdSpendDaily.date >= data_inicio_anterior, AdSpendDaily.date <= data_fim_anterior)
    )
    spend_ant_row = spend_anterior.one()
    gasto_anterior = float(spend_ant_row[0] or 0)
    leads_anterior = spend_ant_row[1] or 0
    
    # --- Métricas de CRM ---
    deals_query = select(
        func.count(CRMDeal.id),
        func.sum(func.cast(CRMDeal.status == DealStatus.GANHO, int)),
        func.sum(func.cast(CRMDeal.status == DealStatus.PERDIDO, int)),
        func.sum(CRMDeal.valor).filter(CRMDeal.status == DealStatus.GANHO),
        func.sum(CRMDeal.lucro_bruto).filter(CRMDeal.status == DealStatus.GANHO)
    ).where(
        CRMDeal.data_criacao >= datetime.combine(data_inicio, datetime.min.time()),
        CRMDeal.data_criacao <= datetime.combine(data_fim, datetime.max.time())
    )
    deals_result = await db.execute(deals_query)
    deals_row = deals_result.one()
    
    deals_total = deals_row[0] or 0
    deals_ganhos = deals_row[1] or 0
    deals_perdidos = deals_row[2] or 0
    receita_total = float(deals_row[3] or 0)
    lucro_bruto = float(deals_row[4] or 0)
    
    # Período anterior
    deals_anterior = await db.execute(
        select(
            func.count(CRMDeal.id),
            func.sum(func.cast(CRMDeal.status == DealStatus.GANHO, int))
        ).where(
            CRMDeal.data_criacao >= datetime.combine(data_inicio_anterior, datetime.min.time()),
            CRMDeal.data_criacao <= datetime.combine(data_fim_anterior, datetime.max.time())
        )
    )
    deals_ant_row = deals_anterior.one()
    deals_total_ant = deals_ant_row[0] or 0
    deals_ganhos_ant = deals_ant_row[1] or 0
    
    # --- Calcular métricas derivadas ---
    taxa_conversao = (deals_ganhos / deals_total * 100) if deals_total > 0 else 0
    taxa_conversao_ant = (deals_ganhos_ant / deals_total_ant * 100) if deals_total_ant > 0 else 0
    
    cpl = gasto_total / leads_total if leads_total > 0 else 0
    cpl_ant = gasto_anterior / leads_anterior if leads_anterior > 0 else 0
    
    cpa = gasto_total / deals_ganhos if deals_ganhos > 0 else 0
    cpa_ant = gasto_anterior / deals_ganhos_ant if deals_ganhos_ant > 0 else 0
    
    roas = receita_total / gasto_total if gasto_total > 0 else 0
    
    # --- Variações ---
    def calc_variacao(atual, anterior):
        if anterior == 0:
            return None
        return ((atual - anterior) / anterior) * 100
    
    # --- Série diária ---
    serie_query = select(
        func.date_trunc('day', CRMDeal.data_criacao).label('dia'),
        func.count(CRMDeal.id).label('deals'),
        func.sum(func.cast(CRMDeal.status == DealStatus.GANHO, int)).label('ganhos')
    ).where(
        CRMDeal.data_criacao >= datetime.combine(data_inicio, datetime.min.time()),
        CRMDeal.data_criacao <= datetime.combine(data_fim, datetime.max.time())
    ).group_by(func.date_trunc('day', CRMDeal.data_criacao)).order_by('dia')
    
    serie_result = await db.execute(serie_query)
    serie_diaria = [
        {
            "data": row.dia.isoformat() if row.dia else None,
            "deals": row.deals or 0,
            "ganhos": row.ganhos or 0
        }
        for row in serie_result.all()
    ]
    
    return DashboardOverview(
        periodo_inicio=data_inicio,
        periodo_fim=data_fim,
        gasto_total=MetricCard(
            label="Gasto Total",
            valor=format_currency(gasto_total),
            variacao=calc_variacao(gasto_total, gasto_anterior),
            variacao_positiva=False  # Menos gasto é melhor
        ),
        leads_total=MetricCard(
            label="Leads",
            valor=format_number(leads_total),
            variacao=calc_variacao(leads_total, leads_anterior),
            variacao_positiva=True
        ),
        deals_total=MetricCard(
            label="Negócios",
            valor=format_number(deals_total),
            variacao=calc_variacao(deals_total, deals_total_ant),
            variacao_positiva=True
        ),
        deals_ganhos=MetricCard(
            label="Vendas",
            valor=format_number(deals_ganhos),
            variacao=calc_variacao(deals_ganhos, deals_ganhos_ant),
            variacao_positiva=True
        ),
        taxa_conversao=MetricCard(
            label="Taxa de Conversão",
            valor=format_percent(taxa_conversao),
            variacao=calc_variacao(taxa_conversao, taxa_conversao_ant),
            variacao_positiva=True
        ),
        cpl=MetricCard(
            label="CPL",
            valor=format_currency(cpl),
            variacao=calc_variacao(cpl, cpl_ant),
            variacao_positiva=False  # Menor é melhor
        ),
        cpa=MetricCard(
            label="CPA",
            valor=format_currency(cpa),
            variacao=calc_variacao(cpa, cpa_ant),
            variacao_positiva=False
        ),
        receita_total=MetricCard(
            label="Receita",
            valor=format_currency(receita_total),
            variacao=None,
            variacao_positiva=True
        ),
        lucro_bruto=MetricCard(
            label="Lucro Bruto",
            valor=format_currency(lucro_bruto),
            variacao=None,
            variacao_positiva=True
        ),
        roas=MetricCard(
            label="ROAS",
            valor=f"{roas:.1f}x",
            variacao=None,
            variacao_positiva=True
        ),
        serie_diaria=serie_diaria
    )


@router.get("/channels", response_model=ChannelComparisonResponse)
async def get_channel_comparison(
    dias: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Comparação de performance entre canais (Google vs Meta)
    """
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias)
    
    canais = []
    
    for platform in [AdPlatform.GOOGLE, AdPlatform.META]:
        # Métricas de ads
        spend_query = select(
            func.sum(AdSpendDaily.spend),
            func.sum(AdSpendDaily.impressions),
            func.sum(AdSpendDaily.clicks),
            func.sum(AdSpendDaily.leads)
        ).where(
            AdSpendDaily.platform == platform,
            AdSpendDaily.date >= data_inicio,
            AdSpendDaily.date <= data_fim
        )
        spend_result = await db.execute(spend_query)
        spend_row = spend_result.one()
        
        gasto = Decimal(str(spend_row[0] or 0))
        impressoes = spend_row[1] or 0
        cliques = spend_row[2] or 0
        leads = spend_row[3] or 0
        
        # Métricas de CRM por canal
        canal_name = "Google" if platform == AdPlatform.GOOGLE else "Meta"
        deals_query = select(
            func.count(CRMDeal.id),
            func.sum(func.cast(CRMDeal.status == DealStatus.GANHO, int)),
            func.sum(CRMDeal.valor).filter(CRMDeal.status == DealStatus.GANHO)
        ).where(
            CRMDeal.canal.ilike(f"%{canal_name}%"),
            CRMDeal.data_criacao >= datetime.combine(data_inicio, datetime.min.time()),
            CRMDeal.data_criacao <= datetime.combine(data_fim, datetime.max.time())
        )
        deals_result = await db.execute(deals_query)
        deals_row = deals_result.one()
        
        deals = deals_row[0] or 0
        deals_ganhos = deals_row[1] or 0
        receita = Decimal(str(deals_row[2] or 0))
        
        taxa_conversao = (deals_ganhos / deals * 100) if deals > 0 else 0
        cpl = gasto / leads if leads > 0 else Decimal(0)
        cpa = gasto / deals_ganhos if deals_ganhos > 0 else Decimal(0)
        roas = receita / gasto if gasto > 0 else None
        
        canais.append(ChannelMetrics(
            canal=platform.value,
            gasto=gasto,
            impressoes=impressoes,
            cliques=cliques,
            leads=leads,
            deals=deals,
            deals_ganhos=deals_ganhos,
            taxa_conversao=taxa_conversao,
            cpl=cpl,
            cpa=cpa,
            receita=receita,
            roas=roas
        ))
    
    return ChannelComparisonResponse(
        periodo_inicio=data_inicio,
        periodo_fim=data_fim,
        canais=canais
    )


@router.get("/vendedores", response_model=VendedorListResponse)
async def get_vendedores_metrics(
    dias: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Métricas por vendedor
    """
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias)
    
    query = select(
        CRMDeal.vendedor,
        func.count(CRMDeal.id).label('total'),
        func.sum(func.cast(CRMDeal.status == DealStatus.GANHO, int)).label('ganhos'),
        func.sum(func.cast(CRMDeal.status == DealStatus.PERDIDO, int)).label('perdidos'),
        func.sum(func.cast(CRMDeal.status == DealStatus.ABERTO, int)).label('abertos'),
        func.sum(CRMDeal.valor).filter(CRMDeal.status == DealStatus.GANHO).label('valor'),
        func.sum(CRMDeal.lucro_bruto).filter(CRMDeal.status == DealStatus.GANHO).label('lucro')
    ).where(
        CRMDeal.data_criacao >= datetime.combine(data_inicio, datetime.min.time()),
        CRMDeal.data_criacao <= datetime.combine(data_fim, datetime.max.time())
    ).group_by(CRMDeal.vendedor).order_by(func.sum(CRMDeal.valor).desc())
    
    result = await db.execute(query)
    
    vendedores = []
    for row in result.all():
        total = row.total or 0
        ganhos = row.ganhos or 0
        perdidos = row.perdidos or 0
        abertos = row.abertos or 0
        valor = Decimal(str(row.valor or 0))
        lucro = Decimal(str(row.lucro or 0))
        
        taxa_conversao = (ganhos / total * 100) if total > 0 else 0
        ticket_medio = valor / ganhos if ganhos > 0 else Decimal(0)
        
        vendedores.append(VendedorMetrics(
            vendedor=row.vendedor,
            deals_total=total,
            deals_ganhos=ganhos,
            deals_perdidos=perdidos,
            deals_abertos=abertos,
            taxa_conversao=taxa_conversao,
            valor_total=valor,
            lucro_bruto=lucro,
            ticket_medio=ticket_medio,
            tempo_medio_fechamento=None  # TODO: calcular
        ))
    
    return VendedorListResponse(
        periodo_inicio=data_inicio,
        periodo_fim=data_fim,
        vendedores=vendedores
    )


@router.get("/funnel", response_model=FunnelMetrics)
async def get_funnel_metrics(
    dias: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Métricas do funil de vendas
    """
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias)
    
    # Leads (de ads)
    leads_result = await db.execute(
        select(func.sum(AdSpendDaily.leads)).where(
            AdSpendDaily.date >= data_inicio,
            AdSpendDaily.date <= data_fim
        )
    )
    total_leads = leads_result.scalar() or 0
    
    # Deals
    deals_query = select(
        func.count(CRMDeal.id).label('total'),
        func.sum(func.cast(CRMDeal.status == DealStatus.GANHO, int)).label('ganhos'),
        func.sum(func.cast(CRMDeal.status == DealStatus.PERDIDO, int)).label('perdidos'),
        func.sum(func.cast(CRMDeal.status == DealStatus.ABERTO, int)).label('abertos')
    ).where(
        CRMDeal.data_criacao >= datetime.combine(data_inicio, datetime.min.time()),
        CRMDeal.data_criacao <= datetime.combine(data_fim, datetime.max.time())
    )
    deals_result = await db.execute(deals_query)
    deals_row = deals_result.one()
    
    total_deals = deals_row.total or 0
    ganhos = deals_row.ganhos or 0
    perdidos = deals_row.perdidos or 0
    abertos = deals_row.abertos or 0
    
    # Motivos de perda
    motivos_query = select(
        CRMDeal.motivo_perda,
        func.count(CRMDeal.id)
    ).where(
        CRMDeal.status == DealStatus.PERDIDO,
        CRMDeal.data_criacao >= datetime.combine(data_inicio, datetime.min.time()),
        CRMDeal.data_criacao <= datetime.combine(data_fim, datetime.max.time()),
        CRMDeal.motivo_perda.isnot(None)
    ).group_by(CRMDeal.motivo_perda).order_by(func.count(CRMDeal.id).desc())
    
    motivos_result = await db.execute(motivos_query)
    motivos_perda = []
    for row in motivos_result.all():
        motivo = row[0] or "Não informado"
        quantidade = row[1]
        percentual = (quantidade / perdidos * 100) if perdidos > 0 else 0
        motivos_perda.append(MotivoPerdaItem(
            motivo=motivo,
            quantidade=quantidade,
            percentual=percentual
        ))
    
    # Taxas
    taxa_lead_to_deal = (total_deals / total_leads * 100) if total_leads > 0 else 0
    taxa_conversao = (ganhos / total_deals * 100) if total_deals > 0 else 0
    taxa_perda = (perdidos / total_deals * 100) if total_deals > 0 else 0
    
    # Série diária
    serie_query = select(
        func.date_trunc('day', CRMDeal.data_criacao).label('dia'),
        func.count(CRMDeal.id).label('total'),
        func.sum(func.cast(CRMDeal.status == DealStatus.GANHO, int)).label('ganhos'),
        func.sum(func.cast(CRMDeal.status == DealStatus.PERDIDO, int)).label('perdidos')
    ).where(
        CRMDeal.data_criacao >= datetime.combine(data_inicio, datetime.min.time()),
        CRMDeal.data_criacao <= datetime.combine(data_fim, datetime.max.time())
    ).group_by(func.date_trunc('day', CRMDeal.data_criacao)).order_by('dia')
    
    serie_result = await db.execute(serie_query)
    serie_diaria = [
        {
            "data": row.dia.isoformat() if row.dia else None,
            "total": row.total or 0,
            "ganhos": row.ganhos or 0,
            "perdidos": row.perdidos or 0
        }
        for row in serie_result.all()
    ]
    
    return FunnelMetrics(
        periodo_inicio=data_inicio,
        periodo_fim=data_fim,
        total_leads=total_leads,
        total_deals=total_deals,
        deals_abertos=abertos,
        deals_ganhos=ganhos,
        deals_perdidos=perdidos,
        taxa_lead_to_deal=taxa_lead_to_deal,
        taxa_conversao=taxa_conversao,
        taxa_perda=taxa_perda,
        motivos_perda=motivos_perda,
        serie_diaria=serie_diaria
    )


@router.get("/kpis")
async def get_kpis(
    dias: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    KPIs resumidos para cards
    """
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias)
    
    # Gastos
    spend = await db.execute(
        select(func.sum(AdSpendDaily.spend), func.sum(AdSpendDaily.leads))
        .where(AdSpendDaily.date >= data_inicio, AdSpendDaily.date <= data_fim)
    )
    spend_row = spend.one()
    gasto_total = float(spend_row[0] or 0)
    leads = spend_row[1] or 0
    
    # Deals
    deals = await db.execute(
        select(
            func.count(CRMDeal.id),
            func.sum(func.cast(CRMDeal.status == DealStatus.GANHO, int)),
            func.sum(CRMDeal.valor).filter(CRMDeal.status == DealStatus.GANHO),
            func.sum(CRMDeal.lucro_bruto).filter(CRMDeal.status == DealStatus.GANHO)
        ).where(
            CRMDeal.data_criacao >= datetime.combine(data_inicio, datetime.min.time()),
            CRMDeal.data_criacao <= datetime.combine(data_fim, datetime.max.time())
        )
    )
    deals_row = deals.one()
    total_deals = deals_row[0] or 0
    ganhos = deals_row[1] or 0
    receita = float(deals_row[2] or 0)
    lucro = float(deals_row[3] or 0)
    
    return {
        "periodo": {"inicio": data_inicio.isoformat(), "fim": data_fim.isoformat()},
        "gasto_total": gasto_total,
        "leads": leads,
        "deals": total_deals,
        "vendas": ganhos,
        "taxa_conversao": (ganhos / total_deals * 100) if total_deals > 0 else 0,
        "cpl": gasto_total / leads if leads > 0 else 0,
        "cpa": gasto_total / ganhos if ganhos > 0 else 0,
        "receita": receita,
        "lucro_bruto": lucro,
        "roas": receita / gasto_total if gasto_total > 0 else 0
    }

