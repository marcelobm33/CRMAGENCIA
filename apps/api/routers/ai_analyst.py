"""
Router da IA Analista
"""
from datetime import datetime, timedelta, date
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from config import get_settings
from models import User
from models.ai import (
    AIRecommendation,
    RecommendationPriority,
    RecommendationScope,
    RecommendationStatus
)
from models.crm import CRMDeal, DealStatus
from models.campaigns import AdSpendDaily
from schemas.ai import (
    AIRecommendationResponse,
    AIRecommendationUpdate,
    AIRecommendationListResponse,
    AIAnalysisRequest,
    AIAnalysisSummary
)
from routers.auth import get_current_user

router = APIRouter()
settings = get_settings()


@router.get("/recommendations", response_model=AIRecommendationListResponse)
async def list_recommendations(
    status_filter: Optional[str] = Query(None, alias="status"),
    prioridade: Optional[str] = None,
    escopo: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista recomendações da IA
    """
    query = select(AIRecommendation)
    
    if status_filter:
        query = query.where(AIRecommendation.status == RecommendationStatus(status_filter))
    
    if prioridade:
        query = query.where(AIRecommendation.prioridade == RecommendationPriority(prioridade))
    
    if escopo:
        query = query.where(AIRecommendation.escopo == RecommendationScope(escopo))
    
    query = query.order_by(AIRecommendation.data.desc()).limit(limit)
    
    result = await db.execute(query)
    recommendations = result.scalars().all()
    
    # Contadores
    pendentes = await db.execute(
        select(func.count(AIRecommendation.id))
        .where(AIRecommendation.status == RecommendationStatus.PENDING)
    )
    em_progresso = await db.execute(
        select(func.count(AIRecommendation.id))
        .where(AIRecommendation.status == RecommendationStatus.IN_PROGRESS)
    )
    
    return AIRecommendationListResponse(
        items=[AIRecommendationResponse.model_validate(r) for r in recommendations],
        total=len(recommendations),
        pendentes=pendentes.scalar() or 0,
        em_progresso=em_progresso.scalar() or 0
    )


@router.get("/recommendations/{recommendation_id}", response_model=AIRecommendationResponse)
async def get_recommendation(
    recommendation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna uma recomendação específica
    """
    result = await db.execute(
        select(AIRecommendation).where(AIRecommendation.id == recommendation_id)
    )
    recommendation = result.scalar_one_or_none()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recomendação não encontrada")
    
    return recommendation


@router.patch("/recommendations/{recommendation_id}", response_model=AIRecommendationResponse)
async def update_recommendation(
    recommendation_id: UUID,
    update_data: AIRecommendationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza status de uma recomendação
    """
    result = await db.execute(
        select(AIRecommendation).where(AIRecommendation.id == recommendation_id)
    )
    recommendation = result.scalar_one_or_none()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recomendação não encontrada")
    
    if update_data.status:
        recommendation.status = RecommendationStatus(update_data.status)
    
    if update_data.notas_usuario is not None:
        recommendation.notas_usuario = update_data.notas_usuario
    
    if update_data.resultado_obtido is not None:
        recommendation.resultado_obtido = update_data.resultado_obtido
    
    await db.commit()
    await db.refresh(recommendation)
    
    return recommendation


@router.post("/analyze", response_model=AIAnalysisSummary)
async def run_analysis(
    request: AIAnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Executa análise e gera novas recomendações
    """
    dias = request.periodo_dias
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias)
    
    recommendations_created = []
    
    # --- Análise 1: Campanhas com CPA muito alto ---
    spend_query = select(
        AdSpendDaily.campaign_external_id,
        func.sum(AdSpendDaily.spend).label('total_spend'),
        func.sum(AdSpendDaily.leads).label('total_leads')
    ).where(
        AdSpendDaily.date >= data_inicio,
        AdSpendDaily.date <= data_fim
    ).group_by(AdSpendDaily.campaign_external_id)
    
    spend_result = await db.execute(spend_query)
    
    for row in spend_result.all():
        if row.total_leads and row.total_leads > 0:
            cpl = float(row.total_spend) / row.total_leads
            if cpl > 100:  # CPL > R$100 é considerado alto
                rec = AIRecommendation(
                    escopo=RecommendationScope.CAMPANHA,
                    prioridade=RecommendationPriority.HIGH if cpl > 200 else RecommendationPriority.MEDIUM,
                    titulo=f"CPL alto na campanha {row.campaign_external_id}",
                    insight=f"A campanha está com CPL de R$ {cpl:.2f}, acima do esperado.",
                    explicacao="Um CPL alto indica que estamos gastando muito para cada lead gerado. Isso pode ser causado por segmentação inadequada, criativos pouco atrativos ou landing page com baixa conversão.",
                    acoes_sugeridas=[
                        {"acao": "Revisar segmentação de público", "tipo": "analise"},
                        {"acao": "Testar novos criativos", "tipo": "teste"},
                        {"acao": "Verificar taxa de conversão da landing page", "tipo": "analise"}
                    ],
                    hipotese="Reduzindo o público ou melhorando os criativos, o CPL pode cair 20-30%",
                    metrica_alvo="CPL",
                    impacto_esperado="Redução de 20-30% no CPL",
                    como_medir="Comparar CPL da próxima semana com esta",
                    contexto_dados={"campaign_id": row.campaign_external_id, "cpl": cpl, "spend": float(row.total_spend), "leads": row.total_leads}
                )
                db.add(rec)
                recommendations_created.append(rec)
    
    # --- Análise 2: Taxa de perda alta ---
    deals_query = select(
        func.count(CRMDeal.id).label('total'),
        func.sum(func.cast(CRMDeal.status == DealStatus.PERDIDO, int)).label('perdidos')
    ).where(
        CRMDeal.data_criacao >= datetime.combine(data_inicio, datetime.min.time()),
        CRMDeal.data_criacao <= datetime.combine(data_fim, datetime.max.time())
    )
    deals_result = await db.execute(deals_query)
    deals_row = deals_result.one()
    
    total_deals = deals_row.total or 0
    perdidos = deals_row.perdidos or 0
    
    if total_deals > 0:
        taxa_perda = (perdidos / total_deals) * 100
        if taxa_perda > 60:
            rec = AIRecommendation(
                escopo=RecommendationScope.CRM,
                prioridade=RecommendationPriority.CRITICAL,
                titulo=f"Taxa de perda muito alta: {taxa_perda:.1f}%",
                insight=f"Nos últimos {dias} dias, {taxa_perda:.1f}% dos negócios foram perdidos.",
                explicacao="Uma taxa de perda acima de 60% indica problemas sérios no processo de vendas. Pode ser qualificação ruim de leads, atendimento demorado, ou preço fora do mercado.",
                acoes_sugeridas=[
                    {"acao": "Analisar motivos de perda mais frequentes", "tipo": "analise"},
                    {"acao": "Verificar tempo médio de resposta aos leads", "tipo": "analise"},
                    {"acao": "Implementar SLA de atendimento", "tipo": "imediata"},
                    {"acao": "Revisar script de vendas", "tipo": "otimizacao"}
                ],
                hipotese="Melhorando o tempo de resposta e qualificação, a taxa de conversão pode dobrar",
                metrica_alvo="Taxa de conversão",
                impacto_esperado="Aumento de 50-100% na taxa de conversão",
                como_medir="Comparar taxa de conversão do próximo mês com este",
                contexto_dados={"total_deals": total_deals, "perdidos": perdidos, "taxa_perda": taxa_perda}
            )
            db.add(rec)
            recommendations_created.append(rec)
    
    # --- Análise 3: Motivos de perda dominantes ---
    motivos_query = select(
        CRMDeal.motivo_perda,
        func.count(CRMDeal.id).label('quantidade')
    ).where(
        CRMDeal.status == DealStatus.PERDIDO,
        CRMDeal.data_criacao >= datetime.combine(data_inicio, datetime.min.time()),
        CRMDeal.data_criacao <= datetime.combine(data_fim, datetime.max.time()),
        CRMDeal.motivo_perda.isnot(None)
    ).group_by(CRMDeal.motivo_perda).order_by(func.count(CRMDeal.id).desc()).limit(3)
    
    motivos_result = await db.execute(motivos_query)
    motivos = motivos_result.all()
    
    if motivos and perdidos > 10:
        top_motivo = motivos[0]
        percentual = (top_motivo.quantidade / perdidos) * 100 if perdidos > 0 else 0
        
        if percentual > 30:
            rec = AIRecommendation(
                escopo=RecommendationScope.ATENDIMENTO,
                prioridade=RecommendationPriority.HIGH,
                titulo=f"Motivo de perda dominante: {top_motivo.motivo_perda}",
                insight=f"O motivo '{top_motivo.motivo_perda}' representa {percentual:.1f}% das perdas ({top_motivo.quantidade} negócios).",
                explicacao=f"Quando um único motivo domina as perdas, é uma oportunidade clara de melhoria. Resolver esse problema pode ter grande impacto nas vendas.",
                acoes_sugeridas=[
                    {"acao": f"Criar plano de ação específico para '{top_motivo.motivo_perda}'", "tipo": "imediata"},
                    {"acao": "Entrevistar vendedores sobre esse motivo", "tipo": "analise"},
                    {"acao": "Revisar processo para evitar essas perdas", "tipo": "otimizacao"}
                ],
                hipotese=f"Reduzindo perdas por '{top_motivo.motivo_perda}' em 50%, podemos ganhar mais {int(top_motivo.quantidade * 0.3)} negócios",
                metrica_alvo="Perdas por motivo específico",
                impacto_esperado=f"Até {int(top_motivo.quantidade * 0.5)} vendas adicionais por período",
                como_medir="Monitorar esse motivo de perda no próximo período",
                contexto_dados={"motivo": top_motivo.motivo_perda, "quantidade": top_motivo.quantidade, "percentual": percentual}
            )
            db.add(rec)
            recommendations_created.append(rec)
    
    # --- Análise 4: Oportunidade em campanha com bom desempenho ---
    good_campaigns_query = select(
        AdSpendDaily.campaign_external_id,
        func.sum(AdSpendDaily.spend).label('total_spend'),
        func.sum(AdSpendDaily.leads).label('total_leads')
    ).where(
        AdSpendDaily.date >= data_inicio,
        AdSpendDaily.date <= data_fim
    ).group_by(AdSpendDaily.campaign_external_id).having(
        func.sum(AdSpendDaily.leads) > 10
    )
    
    good_result = await db.execute(good_campaigns_query)
    
    for row in good_result.all():
        if row.total_leads > 0:
            cpl = float(row.total_spend) / row.total_leads
            if cpl < 30:  # CPL < R$30 é muito bom
                rec = AIRecommendation(
                    escopo=RecommendationScope.ORCAMENTO,
                    prioridade=RecommendationPriority.MEDIUM,
                    titulo=f"Oportunidade: campanha {row.campaign_external_id} com CPL baixo",
                    insight=f"A campanha tem CPL de apenas R$ {cpl:.2f} com {row.total_leads} leads gerados.",
                    explicacao="Campanhas com CPL baixo e volume consistente são candidatas para aumento de orçamento. Escalar antes que a performance degrade.",
                    acoes_sugeridas=[
                        {"acao": "Aumentar orçamento em 20-30%", "tipo": "otimizacao"},
                        {"acao": "Monitorar se CPL se mantém após aumento", "tipo": "analise"}
                    ],
                    hipotese="Aumentando orçamento em 25%, podemos gerar 25% mais leads mantendo o CPL",
                    metrica_alvo="Volume de leads",
                    impacto_esperado=f"Mais {int(row.total_leads * 0.25)} leads por período",
                    como_medir="Acompanhar CPL e volume após aumento",
                    contexto_dados={"campaign_id": row.campaign_external_id, "cpl": cpl, "leads": row.total_leads}
                )
                db.add(rec)
                recommendations_created.append(rec)
    
    await db.commit()
    
    # Contadores
    criticas = sum(1 for r in recommendations_created if r.prioridade == RecommendationPriority.CRITICAL)
    high = sum(1 for r in recommendations_created if r.prioridade == RecommendationPriority.HIGH)
    
    return AIAnalysisSummary(
        periodo_analisado=f"{data_inicio.isoformat()} a {data_fim.isoformat()}",
        total_recomendacoes=len(recommendations_created),
        criticas=criticas,
        oportunidades=sum(1 for r in recommendations_created if r.escopo == RecommendationScope.ORCAMENTO),
        problemas=criticas + high,
        resumo_executivo=f"Análise dos últimos {dias} dias gerou {len(recommendations_created)} recomendações, sendo {criticas} críticas que precisam de ação imediata."
    )


@router.get("/summary")
async def get_ai_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Resumo do estado das recomendações
    """
    # Por status
    status_query = select(
        AIRecommendation.status,
        func.count(AIRecommendation.id)
    ).group_by(AIRecommendation.status)
    status_result = await db.execute(status_query)
    por_status = {row[0].value: row[1] for row in status_result.all()}
    
    # Por prioridade (apenas pendentes)
    prioridade_query = select(
        AIRecommendation.prioridade,
        func.count(AIRecommendation.id)
    ).where(
        AIRecommendation.status == RecommendationStatus.PENDING
    ).group_by(AIRecommendation.prioridade)
    prioridade_result = await db.execute(prioridade_query)
    por_prioridade = {row[0].value: row[1] for row in prioridade_result.all()}
    
    # Por escopo (apenas pendentes)
    escopo_query = select(
        AIRecommendation.escopo,
        func.count(AIRecommendation.id)
    ).where(
        AIRecommendation.status == RecommendationStatus.PENDING
    ).group_by(AIRecommendation.escopo)
    escopo_result = await db.execute(escopo_query)
    por_escopo = {row[0].value: row[1] for row in escopo_result.all()}
    
    # Última análise
    ultima = await db.execute(
        select(AIRecommendation.data).order_by(AIRecommendation.data.desc()).limit(1)
    )
    ultima_analise = ultima.scalar()
    
    return {
        "por_status": por_status,
        "por_prioridade": por_prioridade,
        "por_escopo": por_escopo,
        "ultima_analise": ultima_analise.isoformat() if ultima_analise else None,
        "total_pendentes": por_status.get("pending", 0),
        "criticas_pendentes": por_prioridade.get("critical", 0)
    }

