"""
Tasks da IA Analista
"""
from datetime import datetime, timedelta, date
import json
import structlog

from celery_app import app
from config import get_settings

logger = structlog.get_logger()
settings = get_settings()


@app.task(bind=True)
def run_analysis(self, days: int = 7):
    """
    Executa análise completa e gera recomendações
    """
    logger.info("Iniciando análise da IA", days=days, mode=settings.ai_mode)
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    try:
        # Coletar dados para análise
        context = gather_analysis_context(start_date, end_date)
        
        # Gerar insights
        if settings.ai_mode == "openai" and settings.openai_api_key:
            insights = generate_insights_openai(context)
        else:
            insights = generate_insights_mock(context)
        
        # Salvar recomendações
        recommendations_saved = save_recommendations(insights)
        
        logger.info("Análise concluída", 
            recommendations=recommendations_saved,
            mode=settings.ai_mode
        )
        
        return {
            "status": "success",
            "recommendations": recommendations_saved,
            "mode": settings.ai_mode,
            "period": f"{start_date} - {end_date}"
        }
        
    except Exception as e:
        logger.error("Erro na análise da IA", error=str(e))
        return {"status": "error", "error": str(e)}


@app.task(bind=True)
def analyze_campaign(self, campaign_id: str):
    """
    Análise focada em uma campanha específica
    """
    logger.info("Analisando campanha", campaign_id=campaign_id)
    
    # TODO: Implementar análise específica de campanha
    
    return {"status": "success", "campaign_id": campaign_id}


@app.task(bind=True)
def analyze_vendor(self, vendor_name: str):
    """
    Análise focada em um vendedor específico
    """
    logger.info("Analisando vendedor", vendor=vendor_name)
    
    # TODO: Implementar análise específica de vendedor
    
    return {"status": "success", "vendor": vendor_name}


def gather_analysis_context(start_date: date, end_date: date) -> dict:
    """
    Coleta dados necessários para a análise
    """
    # TODO: Buscar dados reais do banco
    
    return {
        "period": {
            "start": str(start_date),
            "end": str(end_date)
        },
        "metrics": {
            "gasto_total": 8500.00,
            "leads": 180,
            "deals": 120,
            "vendas": 35,
            "receita": 420000.00,
            "cpl": 47.22,
            "cpa": 242.86,
            "taxa_conversao": 29.17
        },
        "by_channel": {
            "google": {"gasto": 4500, "leads": 95, "vendas": 18},
            "meta": {"gasto": 4000, "leads": 85, "vendas": 17}
        },
        "loss_reasons": {
            "Preço alto": 25,
            "Cliente não retornou": 35,
            "Comprou em outro lugar": 15,
            "Outros": 10
        },
        "top_campaigns": [
            {"name": "Busca - Seminovos Premium", "leads": 45, "cpl": 38.00},
            {"name": "Leads - Ofertas Especiais", "leads": 40, "cpl": 42.00}
        ]
    }


def generate_insights_openai(context: dict) -> list:
    """
    Gera insights usando OpenAI API
    """
    import openai
    
    client = openai.OpenAI(api_key=settings.openai_api_key)
    
    prompt = f"""
    Você é um analista de performance de marketing digital para uma revenda de carros.
    
    Analise os seguintes dados dos últimos dias e gere recomendações práticas:
    
    {json.dumps(context, indent=2, ensure_ascii=False)}
    
    Para cada problema ou oportunidade identificada, forneça:
    1. O que você observou (insight)
    2. O que isso significa
    3. Ações práticas sugeridas
    4. Hipótese de melhoria
    5. Como medir o resultado
    
    Retorne em formato JSON com a estrutura:
    [
        {{
            "escopo": "campanha|criativo|publico|orcamento|atendimento|crm",
            "prioridade": "critical|high|medium|low",
            "titulo": "título curto",
            "insight": "o que você viu",
            "explicacao": "o que significa",
            "acoes_sugeridas": [{{"acao": "...", "tipo": "imediata|teste|otimizacao"}}],
            "hipotese": "se X então Y",
            "metrica_alvo": "qual métrica melhorar",
            "impacto_esperado": "quanto pode melhorar",
            "como_medir": "como saber se funcionou"
        }}
    ]
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "Você é um analista experiente de marketing digital."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    result = json.loads(response.choices[0].message.content)
    return result.get("recommendations", result) if isinstance(result, dict) else result


def generate_insights_mock(context: dict) -> list:
    """
    Gera insights usando regras simples (modo mock)
    """
    insights = []
    
    metrics = context.get("metrics", {})
    loss_reasons = context.get("loss_reasons", {})
    
    # Regra 1: Taxa de conversão baixa
    if metrics.get("taxa_conversao", 0) < 25:
        insights.append({
            "escopo": "crm",
            "prioridade": "high",
            "titulo": f"Taxa de conversão abaixo do ideal: {metrics.get('taxa_conversao', 0):.1f}%",
            "insight": "A taxa de conversão está abaixo de 25%, indicando problemas no funil de vendas.",
            "explicacao": "Leads qualificados não estão convertendo em vendas na taxa esperada.",
            "acoes_sugeridas": [
                {"acao": "Analisar tempo de primeira resposta", "tipo": "analise"},
                {"acao": "Implementar follow-up automatizado", "tipo": "otimizacao"}
            ],
            "hipotese": "Melhorando o tempo de resposta, a conversão pode aumentar 20%",
            "metrica_alvo": "Taxa de conversão",
            "impacto_esperado": "Aumento de 5-10 pontos percentuais",
            "como_medir": "Comparar taxa de conversão mensal"
        })
    
    # Regra 2: Muitas perdas por falta de retorno
    no_response = loss_reasons.get("Cliente não retornou", 0)
    total_losses = sum(loss_reasons.values())
    if total_losses > 0 and (no_response / total_losses) > 0.3:
        insights.append({
            "escopo": "atendimento",
            "prioridade": "critical",
            "titulo": f"Alto índice de 'cliente não retornou': {no_response} casos",
            "insight": f"{(no_response/total_losses*100):.0f}% das perdas são por falta de retorno do cliente.",
            "explicacao": "Clientes perdendo interesse pode indicar atendimento lento ou follow-up inexistente.",
            "acoes_sugeridas": [
                {"acao": "Definir SLA máximo de 30 min para primeiro contato", "tipo": "imediata"},
                {"acao": "Criar sequência de 5 follow-ups", "tipo": "otimizacao"},
                {"acao": "Implementar WhatsApp Business API", "tipo": "otimizacao"}
            ],
            "hipotese": "Com atendimento rápido, podemos recuperar 30% desses leads",
            "metrica_alvo": "Perdas por não retorno",
            "impacto_esperado": f"Recuperar {int(no_response * 0.3)} negócios por período",
            "como_medir": "Monitorar motivo de perda e tempo de primeira resposta"
        })
    
    # Regra 3: CPL alto
    if metrics.get("cpl", 0) > 60:
        insights.append({
            "escopo": "campanha",
            "prioridade": "medium",
            "titulo": f"CPL médio elevado: R$ {metrics.get('cpl', 0):.2f}",
            "insight": "O custo por lead está acima de R$ 60, impactando a margem.",
            "explicacao": "CPL alto reduz o retorno sobre investimento em marketing.",
            "acoes_sugeridas": [
                {"acao": "Revisar segmentação das campanhas", "tipo": "analise"},
                {"acao": "Testar novos criativos", "tipo": "teste"},
                {"acao": "Otimizar landing pages", "tipo": "otimizacao"}
            ],
            "hipotese": "Otimizando campanhas, o CPL pode cair 20%",
            "metrica_alvo": "CPL",
            "impacto_esperado": f"Economia de R$ {metrics.get('gasto_total', 0) * 0.2:.2f}",
            "como_medir": "Comparar CPL semanal"
        })
    
    return insights


def save_recommendations(insights: list) -> int:
    """
    Salva recomendações no banco de dados
    """
    # TODO: Implementar salvamento real no banco
    logger.info("Salvando recomendações", count=len(insights))
    
    for insight in insights:
        logger.debug("Recomendação", 
            titulo=insight.get("titulo"),
            prioridade=insight.get("prioridade")
        )
    
    return len(insights)

