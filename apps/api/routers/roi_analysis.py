"""
Router para análise de ROI - Cruzamento CRM vs Agência
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends
import structlog

from services.external_crm import get_external_crm, ExternalCRMClient
from schemas.agency import (
    AgencyReportCreate,
    AgencyReportResponse,
    ROIAnalysisResponse,
    DashboardCruzamentoResponse
)

logger = structlog.get_logger()
router = APIRouter(prefix="/roi", tags=["ROI Analysis"])


# Dados da agência em memória (depois migrar para banco)
AGENCY_DATA = {
    "2025-10": {
        "investimento_meta": 8500,
        "investimento_google": 7000,
        "investimento_total": 15500,
        "meta_conversoes": 322,
        "meta_cliques": 56957,
        "meta_alcance": 1001041,
        "google_conversoes": 244,
        "google_cliques": 5799,
        "total_leads_reportados": 431,
        "total_vendas_reportadas": 36
    },
    "2025-11": {
        "investimento_meta": 8914,
        "investimento_google": 6714,
        "investimento_total": 15628,
        "meta_conversoes": 330,
        "meta_cliques": 39687,
        "meta_alcance": 830497,
        "google_conversoes": 244,
        "google_cliques": 5799,
        "total_leads_reportados": 359,
        "total_vendas_reportadas": 40
    },
    "2025-12": {
        "investimento_meta": 8491,
        "investimento_google": 6979,
        "investimento_total": 15470,
        "meta_conversoes": 136,
        "meta_cliques": 37050,
        "meta_alcance": 634051,
        "meta_impressoes": 1578803,
        "meta_engajamento": 312029,
        "meta_visitas_perfil": 4628,
        "google_conversoes": 248,
        "google_cliques": 5224,
        "google_impressoes": 98814,
        "google_chamadas": 19,
        "google_whatsapp": 136,
        "google_visitas_loja": 93,
        "google_custo_conversao": 28,
        "total_leads_reportados": 341,
        "total_vendas_reportadas": 38,
        "instagram_novos_seguidores": 412,
        "instagram_publicacoes": 9,
        "instagram_stories": 5,
        "instagram_likes": 408,
        "instagram_comentarios": 29
    }
}


def get_periodo_key(ano: int, mes: int) -> str:
    return f"{ano}-{mes:02d}"


@router.get("/dashboard/{ano}/{mes}", response_model=DashboardCruzamentoResponse)
async def get_dashboard_cruzamento(ano: int, mes: int):
    """
    Dashboard principal de cruzamento CRM vs Agência
    Mostra a verdade: o que a agência reporta vs o que realmente aconteceu
    """
    periodo_key = get_periodo_key(ano, mes)
    
    # Buscar dados da agência
    agencia = AGENCY_DATA.get(periodo_key, {})
    if not agencia:
        raise HTTPException(
            status_code=404, 
            detail=f"Dados da agência não encontrados para {periodo_key}"
        )
    
    # Buscar dados reais do CRM
    try:
        crm = get_external_crm()
        
        # Período do mês
        if mes == 12:
            data_fim = date(ano + 1, 1, 1)
        else:
            data_fim = date(ano, mes + 1, 1)
        data_inicio = date(ano, mes, 1)
        
        # Buscar resumo por origem
        resumo_origem = crm.get_resumo_por_origem(data_inicio, data_fim)
        
        # Buscar resumo geral do mês
        resumo_mes = crm.get_resumo_mensal(ano, mes)
        
        # Separar por canal
        meta_data = next((r for r in resumo_origem if r.get('grupo_origem') == 'META'), {})
        google_data = next((r for r in resumo_origem if r.get('grupo_origem') == 'GOOGLE'), {})
        
    except Exception as e:
        logger.error("Erro ao buscar dados do CRM", error=str(e))
        # Usar dados mockados se CRM falhar
        resumo_mes = {
            "total_leads": 0,
            "ganhos": 0,
            "perdidos": 0,
            "valor_vendido": 0,
            "taxa_conversao": 0
        }
        meta_data = {}
        google_data = {}
    
    # Calcular métricas reais
    leads_crm_total = resumo_mes.get('total_leads', 0)
    vendas_crm = resumo_mes.get('ganhos', 0)
    valor_vendido = float(resumo_mes.get('valor_vendido', 0))
    
    leads_meta = meta_data.get('total_leads', 0)
    vendas_meta = meta_data.get('ganhos', 0)
    valor_meta = float(meta_data.get('valor_vendido', 0))
    
    leads_google = google_data.get('total_leads', 0)
    vendas_google = google_data.get('ganhos', 0)
    valor_google = float(google_data.get('valor_vendido', 0))
    
    investimento_total = agencia.get('investimento_total', 0)
    investimento_meta = agencia.get('investimento_meta', 0)
    investimento_google = agencia.get('investimento_google', 0)
    
    leads_agencia = agencia.get('total_leads_reportados', 0)
    
    # Cálculos de ROI
    custo_por_lead_agencia = investimento_total / leads_agencia if leads_agencia > 0 else 0
    custo_por_lead_real = investimento_total / leads_crm_total if leads_crm_total > 0 else 0
    custo_por_venda = investimento_total / vendas_crm if vendas_crm > 0 else 0
    roi_percentual = (valor_vendido / investimento_total * 100) if investimento_total > 0 else 0
    
    # META específico
    cpl_meta = investimento_meta / leads_meta if leads_meta > 0 else 0
    cpv_meta = investimento_meta / vendas_meta if vendas_meta > 0 else 0
    roi_meta = (valor_meta / investimento_meta * 100) if investimento_meta > 0 else 0
    
    # GOOGLE específico
    cpl_google = investimento_google / leads_google if leads_google > 0 else 0
    cpv_google = investimento_google / vendas_google if vendas_google > 0 else 0
    roi_google = (valor_google / investimento_google * 100) if investimento_google > 0 else 0
    
    # Gerar alertas
    alertas = []
    
    diferenca_leads = leads_agencia - leads_crm_total
    if diferenca_leads > 50:
        alertas.append(f"⚠️ Agência reporta {diferenca_leads} leads a mais que o CRM registra")
    
    if custo_por_venda > 1000:
        alertas.append(f"🔴 Custo por venda alto: R$ {custo_por_venda:,.2f}")
    
    taxa_conversao = (vendas_crm / leads_crm_total * 100) if leads_crm_total > 0 else 0
    if taxa_conversao < 10:
        alertas.append(f"📉 Taxa de conversão baixa: {taxa_conversao:.1f}%")
    
    # Gerar insights
    insights = []
    
    if roi_google > roi_meta:
        insights.append(f"💡 Google está {(roi_google/roi_meta - 1)*100:.0f}% mais eficiente que Meta em ROI")
    elif roi_meta > roi_google:
        insights.append(f"💡 Meta está {(roi_meta/roi_google - 1)*100:.0f}% mais eficiente que Google em ROI")
    
    if cpv_google < cpv_meta and cpv_google > 0:
        economia = cpv_meta - cpv_google
        insights.append(f"💰 Google tem custo por venda R$ {economia:,.2f} menor que Meta")
    
    if vendas_crm > 0:
        ticket_medio = valor_vendido / vendas_crm
        insights.append(f"🎯 Ticket médio: R$ {ticket_medio:,.2f}")
    
    # Montar resposta
    return {
        "periodo": f"{mes:02d}/{ano}",
        "investimento_total": investimento_total,
        "leads_agencia": leads_agencia,
        "leads_crm": leads_crm_total,
        "vendas_crm": vendas_crm,
        "valor_vendido": valor_vendido,
        "custo_por_lead_agencia": round(custo_por_lead_agencia, 2),
        "custo_por_lead_real": round(custo_por_lead_real, 2),
        "custo_por_venda": round(custo_por_venda, 2),
        "roi_percentual": round(roi_percentual, 2),
        "meta": {
            "investimento": investimento_meta,
            "leads_agencia": agencia.get('meta_conversoes', 0),
            "leads_crm": leads_meta,
            "vendas": vendas_meta,
            "valor_vendido": valor_meta,
            "custo_por_lead": round(cpl_meta, 2),
            "custo_por_venda": round(cpv_meta, 2),
            "roi": round(roi_meta, 2),
            "alcance": agencia.get('meta_alcance', 0),
            "cliques": agencia.get('meta_cliques', 0)
        },
        "google": {
            "investimento": investimento_google,
            "leads_agencia": agencia.get('google_conversoes', 0),
            "leads_crm": leads_google,
            "vendas": vendas_google,
            "valor_vendido": valor_google,
            "custo_por_lead": round(cpl_google, 2),
            "custo_por_venda": round(cpv_google, 2),
            "roi": round(roi_google, 2),
            "cliques": agencia.get('google_cliques', 0),
            "whatsapp": agencia.get('google_whatsapp', 0)
        },
        "funil": {
            "leads_total": leads_crm_total,
            "em_andamento": resumo_mes.get('em_andamento', 0),
            "ganhos": vendas_crm,
            "perdidos": resumo_mes.get('perdidos', 0),
            "taxa_conversao": round(taxa_conversao, 2)
        },
        "alertas": alertas,
        "insights": insights
    }


@router.get("/comparativo-semestral")
async def get_comparativo_semestral():
    """
    Comparativo dos últimos 6 meses - Tendências
    """
    resultados = []
    
    # Pegar dados de Jul-Dez 2025
    meses = [
        (2025, 7), (2025, 8), (2025, 9),
        (2025, 10), (2025, 11), (2025, 12)
    ]
    
    try:
        crm = get_external_crm()
        
        for ano, mes in meses:
            periodo_key = get_periodo_key(ano, mes)
            agencia = AGENCY_DATA.get(periodo_key, {})
            
            # Período
            if mes == 12:
                data_fim = date(ano + 1, 1, 1)
            else:
                data_fim = date(ano, mes + 1, 1)
            data_inicio = date(ano, mes, 1)
            
            resumo = crm.get_resumo_mensal(ano, mes)
            
            investimento = agencia.get('investimento_total', 0)
            vendas = resumo.get('ganhos', 0) if resumo else 0
            valor = float(resumo.get('valor_vendido', 0)) if resumo else 0
            leads = resumo.get('total_leads', 0) if resumo else 0
            
            resultados.append({
                "periodo": f"{mes:02d}/{ano}",
                "ano": ano,
                "mes": mes,
                "investimento": investimento,
                "leads_agencia": agencia.get('total_leads_reportados', 0),
                "leads_crm": leads,
                "vendas": vendas,
                "valor_vendido": valor,
                "custo_por_venda": investimento / vendas if vendas > 0 else 0,
                "roi": (valor / investimento * 100) if investimento > 0 else 0
            })
    except Exception as e:
        logger.error("Erro ao buscar comparativo", error=str(e))
    
    return {
        "periodos": resultados,
        "resumo": {
            "investimento_total": sum(r['investimento'] for r in resultados),
            "vendas_total": sum(r['vendas'] for r in resultados),
            "valor_total": sum(r['valor_vendido'] for r in resultados),
            "roi_medio": sum(r['roi'] for r in resultados) / len(resultados) if resultados else 0
        }
    }


@router.post("/agencia/report")
async def create_agency_report(report: AgencyReportCreate):
    """
    Cadastrar relatório mensal da agência
    """
    periodo_key = get_periodo_key(report.ano, report.mes)
    
    # Calcular total
    investimento_total = (
        float(report.investimento_meta) + 
        float(report.investimento_google) + 
        float(report.investimento_tiktok) + 
        float(report.investimento_outros)
    )
    
    AGENCY_DATA[periodo_key] = {
        "investimento_meta": float(report.investimento_meta),
        "investimento_google": float(report.investimento_google),
        "investimento_tiktok": float(report.investimento_tiktok),
        "investimento_outros": float(report.investimento_outros),
        "investimento_total": investimento_total,
        "meta_conversoes": report.meta_conversoes,
        "meta_cliques": report.meta_cliques,
        "meta_alcance": report.meta_alcance,
        "meta_impressoes": report.meta_impressoes,
        "meta_visitas_perfil": report.meta_visitas_perfil,
        "google_conversoes": report.google_conversoes,
        "google_cliques": report.google_cliques,
        "google_impressoes": report.google_impressoes,
        "google_chamadas": report.google_chamadas,
        "google_whatsapp": report.google_whatsapp,
        "google_visitas_loja": report.google_visitas_loja,
        "google_custo_conversao": float(report.google_custo_conversao),
        "total_leads_reportados": report.total_leads_reportados,
        "total_vendas_reportadas": report.total_vendas_reportadas,
        "instagram_novos_seguidores": report.instagram_novos_seguidores,
        "instagram_publicacoes": report.instagram_publicacoes,
        "instagram_stories": report.instagram_stories,
        "instagram_likes": report.instagram_likes
    }
    
    return {
        "message": f"Relatório {periodo_key} cadastrado com sucesso",
        "data": AGENCY_DATA[periodo_key]
    }


@router.get("/agencia/reports")
async def list_agency_reports():
    """
    Listar todos os relatórios da agência cadastrados
    """
    return {
        "reports": [
            {"periodo": k, **v} for k, v in sorted(AGENCY_DATA.items(), reverse=True)
        ]
    }


@router.get("/insights/{ano}/{mes}")
async def get_insights_detalhados(ano: int, mes: int):
    """
    Insights detalhados e recomendações para o mês
    """
    periodo_key = get_periodo_key(ano, mes)
    agencia = AGENCY_DATA.get(periodo_key, {})
    
    if not agencia:
        raise HTTPException(status_code=404, detail="Dados não encontrados")
    
    try:
        crm = get_external_crm()
        
        # Período
        if mes == 12:
            data_fim = date(ano + 1, 1, 1)
        else:
            data_fim = date(ano, mes + 1, 1)
        data_inicio = date(ano, mes, 1)
        
        resumo_origem = crm.get_resumo_por_origem(data_inicio, data_fim)
        resumo_vendedor = crm.get_resumo_por_vendedor(data_inicio, data_fim)
        motivos_perda = crm.get_motivos_perda(data_inicio, data_fim)
        resumo_mes = crm.get_resumo_mensal(ano, mes)
        
    except Exception as e:
        logger.error("Erro ao buscar insights", error=str(e))
        raise HTTPException(status_code=500, detail="Erro ao buscar dados do CRM")
    
    # Gerar insights
    insights = []
    recomendacoes = []
    
    # Análise de origens
    meta_data = next((r for r in resumo_origem if r.get('grupo_origem') == 'META'), {})
    google_data = next((r for r in resumo_origem if r.get('grupo_origem') == 'GOOGLE'), {})
    
    inv_meta = agencia.get('investimento_meta', 0)
    inv_google = agencia.get('investimento_google', 0)
    
    vendas_meta = meta_data.get('ganhos', 0)
    vendas_google = google_data.get('ganhos', 0)
    
    cpv_meta = inv_meta / vendas_meta if vendas_meta > 0 else float('inf')
    cpv_google = inv_google / vendas_google if vendas_google > 0 else float('inf')
    
    if cpv_google < cpv_meta and cpv_google > 0 and cpv_meta < float('inf'):
        economia_potencial = (cpv_meta - cpv_google) * vendas_meta
        insights.append({
            "tipo": "oportunidade",
            "titulo": "Google mais eficiente",
            "descricao": f"Google tem custo por venda R$ {cpv_meta - cpv_google:,.2f} menor que Meta",
            "impacto": f"Economia potencial de R$ {economia_potencial:,.2f} se realocar budget"
        })
        recomendacoes.append({
            "acao": "Realocar 20% do budget de Meta para Google",
            "expectativa": f"Redução de R$ {economia_potencial * 0.2:,.2f} no custo total",
            "prioridade": "alta"
        })
    
    # Análise de vendedores
    if resumo_vendedor:
        melhor = max(resumo_vendedor, key=lambda x: x.get('taxa_conversao', 0))
        pior = min(resumo_vendedor, key=lambda x: x.get('taxa_conversao', 100))
        
        if melhor.get('taxa_conversao', 0) > pior.get('taxa_conversao', 0) * 2:
            insights.append({
                "tipo": "alerta",
                "titulo": "Disparidade de performance",
                "descricao": f"{melhor.get('vendedor')} converte {melhor.get('taxa_conversao'):.1f}% vs {pior.get('vendedor')} com {pior.get('taxa_conversao'):.1f}%",
                "impacto": "Oportunidade de treinamento"
            })
            recomendacoes.append({
                "acao": f"Treinar {pior.get('vendedor')} com metodologia de {melhor.get('vendedor')}",
                "expectativa": "Aumento de conversão do time",
                "prioridade": "media"
            })
    
    # Análise de motivos de perda
    if motivos_perda:
        principal = motivos_perda[0]
        insights.append({
            "tipo": "info",
            "titulo": "Principal motivo de perda",
            "descricao": f"'{principal.get('motivo_perda')}' representa {principal.get('percentual', 0):.1f}% das perdas",
            "impacto": f"{principal.get('quantidade', 0)} negócios perdidos"
        })
    
    # Análise de discrepância agência vs CRM
    leads_agencia = agencia.get('total_leads_reportados', 0)
    leads_crm = resumo_mes.get('total_leads', 0)
    
    if leads_agencia > 0 and leads_crm > 0:
        diferenca = leads_agencia - leads_crm
        percentual = (diferenca / leads_agencia) * 100
        
        if percentual > 20:
            insights.append({
                "tipo": "alerta",
                "titulo": "Discrepância de leads",
                "descricao": f"Agência reporta {leads_agencia} leads, CRM mostra {leads_crm} ({percentual:.0f}% diferença)",
                "impacto": "Possível perda de leads ou contagem duplicada"
            })
            recomendacoes.append({
                "acao": "Auditar origem dos leads com a agência",
                "expectativa": "Identificar onde leads estão se perdendo",
                "prioridade": "alta"
            })
    
    return {
        "periodo": f"{mes:02d}/{ano}",
        "insights": insights,
        "recomendacoes": recomendacoes,
        "dados": {
            "por_origem": resumo_origem,
            "por_vendedor": resumo_vendedor,
            "motivos_perda": motivos_perda[:5],
            "resumo_mes": resumo_mes
        }
    }
