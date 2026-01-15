"""
API Standalone para Dashboard de ROI
Conecta diretamente ao CRM MySQL, sem depender de PostgreSQL
CORRIGIDO: Considera tanto ORIGEM quanto CANAL como fonte de mídia
"""
import os
import calendar
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pymysql
from pymysql.cursors import DictCursor

# Configurações do CRM
CRM_HOST = os.getenv("EXTERNAL_CRM_HOST", "mysql.netcar-rc.com.br")
CRM_PORT = int(os.getenv("EXTERNAL_CRM_PORT", "3306"))
CRM_DATABASE = os.getenv("EXTERNAL_CRM_DATABASE", "netcarrc01")
CRM_USER = os.getenv("EXTERNAL_CRM_USER", "netcarrc01_add1")
CRM_PASSWORD = os.getenv("EXTERNAL_CRM_PASSWORD", "Banco@netcar")

# Dados da agência (Voren) - Atualizado com dados dos relatórios
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
        "google_conversoes": 248,
        "google_cliques": 5224,
        "google_impressoes": 98814,
        "google_chamadas": 19,
        "google_whatsapp": 136,
        "total_leads_reportados": 341,
        "total_vendas_reportadas": 38
    },
    "2026-01": {
        "investimento_meta": 8500,  # Estimativa
        "investimento_google": 7000,  # Estimativa
        "investimento_total": 15500,
        "meta_conversoes": 0,
        "google_conversoes": 0,
        "total_leads_reportados": 0,
        "total_vendas_reportadas": 0
    }
}

app = FastAPI(
    title="ROI Dashboard API",
    description="API para análise de ROI - CRM vs Agência (considera origem E canal)",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_crm_connection():
    """Conecta ao CRM MySQL"""
    return pymysql.connect(
        host=CRM_HOST,
        port=CRM_PORT,
        database=CRM_DATABASE,
        user=CRM_USER,
        password=CRM_PASSWORD,
        cursorclass=DictCursor,
        charset='utf8mb4'
    )


def get_resumo_mes(ano: int, mes: int) -> dict:
    """Busca resumo do mês no CRM"""
    conn = get_crm_connection()
    try:
        query = """
        SELECT 
            COUNT(*) AS total_leads,
            SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
            SUM(CASE WHEN id_state BETWEEN 1 AND 5 THEN 1 ELSE 0 END) AS em_andamento,
            SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) AS valor_vendido,
            ROUND(AVG(CASE WHEN id_state = 6 THEN valor ELSE NULL END), 2) AS ticket_medio
        FROM crm_negocio
        WHERE YEAR(date_create) = %s AND MONTH(date_create) = %s
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (ano, mes))
            result = cursor.fetchone()
        
        ganhos = result['ganhos'] or 0
        perdidos = result['perdidos'] or 0
        total = ganhos + perdidos
        taxa = (ganhos / total * 100) if total > 0 else 0
        
        return {
            'total_leads': result['total_leads'] or 0,
            'ganhos': ganhos,
            'perdidos': perdidos,
            'em_andamento': result['em_andamento'] or 0,
            'valor_vendido': float(result['valor_vendido'] or 0),
            'ticket_medio': float(result['ticket_medio'] or 0),
            'taxa_conversao': round(taxa, 2)
        }
    finally:
        conn.close()


def get_resumo_midia_paga(ano: int, mes: int) -> dict:
    """
    Busca resumo de mídia paga considerando ORIGEM ou CANAL
    CORRIGIDO: Um lead é considerado de mídia paga se origem OU canal for Instagram/Facebook/Google
    """
    conn = get_crm_connection()
    try:
        # Query corrigida: considera origem OU canal
        query = """
        SELECT 
            CASE 
                WHEN origem = 'INSTAGRAM' OR canal = 'INSTAGRAM' THEN 'INSTAGRAM'
                WHEN origem = 'FACEBOOK' OR canal = 'FACEBOOK' THEN 'FACEBOOK'
                WHEN origem = 'GOOGLE' OR canal = 'GOOGLE' THEN 'GOOGLE'
            END AS plataforma,
            COUNT(*) AS total_leads,
            SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
            SUM(CASE WHEN id_state BETWEEN 1 AND 5 THEN 1 ELSE 0 END) AS em_andamento,
            SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) AS valor_vendido
        FROM crm_negocio
        WHERE (origem IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE') 
               OR canal IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE'))
          AND YEAR(date_create) = %s AND MONTH(date_create) = %s
        GROUP BY plataforma
        ORDER BY ganhos DESC
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (ano, mes))
            results = cursor.fetchall()
        
        dados = {
            'INSTAGRAM': {'leads': 0, 'vendas': 0, 'valor': 0, 'perdidos': 0},
            'FACEBOOK': {'leads': 0, 'vendas': 0, 'valor': 0, 'perdidos': 0},
            'GOOGLE': {'leads': 0, 'vendas': 0, 'valor': 0, 'perdidos': 0}
        }
        
        for r in results:
            if r['plataforma'] in dados:
                dados[r['plataforma']] = {
                    'leads': r['total_leads'] or 0,
                    'vendas': r['ganhos'] or 0,
                    'valor': float(r['valor_vendido'] or 0),
                    'perdidos': r['perdidos'] or 0
                }
        
        return dados
    finally:
        conn.close()


def _parse_ymd(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def _month_fraction_for_range(year: int, month: int, start: date, end: date) -> float:
    """Retorna fração do mês incluída dentro do range [start, end]."""
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    s = max(start, first_day)
    e = min(end, last_day)
    if e < s:
        return 0.0
    days_in_month = (last_day - first_day).days + 1
    days_in_range = (e - s).days + 1
    return days_in_range / days_in_month


def _agency_sum_for_range(start: date, end: date) -> dict:
    """Soma (e pró-rateia) investimento/leads reportados da agência no período."""
    # meses envolvidos
    year_months = []
    y, m = start.year, start.month
    while (y < end.year) or (y == end.year and m <= end.month):
        year_months.append((y, m))
        m += 1
        if m == 13:
            m = 1
            y += 1

    tot = {
        "investimento_total": 0.0,
        "investimento_meta": 0.0,
        "investimento_google": 0.0,
        "leads_reportados": 0.0,
        "meta_leads_reportados": 0.0,
        "google_leads_reportados": 0.0,
        "meta_cliques": 0.0,
        "meta_alcance": 0.0,
        "google_cliques": 0.0,
        "google_whatsapp": 0.0,
    }

    for y, m in year_months:
        key = f"{y}-{m:02d}"
        month_data = AGENCY_DATA.get(key)
        if not month_data:
            continue
        frac = _month_fraction_for_range(y, m, start, end)
        if frac <= 0:
            continue

        tot["investimento_total"] += float(month_data.get("investimento_total", 0)) * frac
        tot["investimento_meta"] += float(month_data.get("investimento_meta", 0)) * frac
        tot["investimento_google"] += float(month_data.get("investimento_google", 0)) * frac

        tot["leads_reportados"] += float(month_data.get("total_leads_reportados", 0)) * frac
        tot["meta_leads_reportados"] += float(month_data.get("meta_conversoes", 0)) * frac
        tot["google_leads_reportados"] += float(month_data.get("google_conversoes", 0)) * frac

        tot["meta_cliques"] += float(month_data.get("meta_cliques", 0)) * frac
        tot["meta_alcance"] += float(month_data.get("meta_alcance", 0)) * frac
        tot["google_cliques"] += float(month_data.get("google_cliques", 0)) * frac
        tot["google_whatsapp"] += float(month_data.get("google_whatsapp", 0)) * frac

    return tot


def get_resumo_mes_range(start: date, end: date) -> dict:
    """Resumo do CRM no período (por date_create)."""
    conn = get_crm_connection()
    try:
        query = """
        SELECT 
            COUNT(*) AS total_leads,
            SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
            SUM(CASE WHEN id_state BETWEEN 1 AND 5 THEN 1 ELSE 0 END) AS em_andamento,
            SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) AS valor_vendido,
            ROUND(AVG(CASE WHEN id_state = 6 THEN valor ELSE NULL END), 2) AS ticket_medio
        FROM crm_negocio
        WHERE date_create >= %s AND date_create <= %s
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (start, end))
            result = cursor.fetchone()

        ganhos = int(result["ganhos"] or 0)
        perdidos = int(result["perdidos"] or 0)
        total = ganhos + perdidos
        taxa = (ganhos / total * 100) if total > 0 else 0

        return {
            "total_leads": int(result["total_leads"] or 0),
            "ganhos": ganhos,
            "perdidos": perdidos,
            "em_andamento": int(result["em_andamento"] or 0),
            "valor_vendido": float(result["valor_vendido"] or 0),
            "ticket_medio": float(result["ticket_medio"] or 0),
            "taxa_conversao": round(taxa, 2),
        }
    finally:
        conn.close()


def get_resumo_midia_paga_range(start: date, end: date) -> dict:
    """Resumo de mídia paga no período (origem OU canal)."""
    conn = get_crm_connection()
    try:
        query = """
        SELECT 
            CASE 
                WHEN origem = 'INSTAGRAM' OR canal = 'INSTAGRAM' THEN 'INSTAGRAM'
                WHEN origem = 'FACEBOOK' OR canal = 'FACEBOOK' THEN 'FACEBOOK'
                WHEN origem = 'GOOGLE' OR canal = 'GOOGLE' THEN 'GOOGLE'
            END AS plataforma,
            COUNT(*) AS total_leads,
            SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
            SUM(CASE WHEN id_state BETWEEN 1 AND 5 THEN 1 ELSE 0 END) AS em_andamento,
            SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) AS valor_vendido
        FROM crm_negocio
        WHERE (origem IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE') 
               OR canal IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE'))
          AND date_create >= %s AND date_create <= %s
        GROUP BY plataforma
        ORDER BY ganhos DESC
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (start, end))
            results = cursor.fetchall()

        dados = {
            "INSTAGRAM": {"leads": 0, "vendas": 0, "valor": 0.0, "perdidos": 0},
            "FACEBOOK": {"leads": 0, "vendas": 0, "valor": 0.0, "perdidos": 0},
            "GOOGLE": {"leads": 0, "vendas": 0, "valor": 0.0, "perdidos": 0},
        }

        for r in results:
            plat = r.get("plataforma")
            if plat in dados:
                dados[plat] = {
                    "leads": int(r["total_leads"] or 0),
                    "vendas": int(r["ganhos"] or 0),
                    "valor": float(r["valor_vendido"] or 0),
                    "perdidos": int(r["perdidos"] or 0),
                }

        return dados
    finally:
        conn.close()


def get_vendas_midia_range(start: date, end: date) -> list:
    """Vendas detalhadas de mídia paga no período (origem OU canal)."""
    conn = get_crm_connection()
    try:
        query = """
        SELECT 
            n.id_crm_negocio AS id,
            n.origem,
            n.canal,
            CASE 
                WHEN n.origem = 'INSTAGRAM' OR n.canal = 'INSTAGRAM' THEN 'INSTAGRAM'
                WHEN n.origem = 'FACEBOOK' OR n.canal = 'FACEBOOK' THEN 'FACEBOOK'
                WHEN n.origem = 'GOOGLE' OR n.canal = 'GOOGLE' THEN 'GOOGLE'
            END AS plataforma,
            n.titulo AS veiculo,
            n.cliente,
            u.name AS vendedor,
            n.valor,
            n.date_create AS entrada,
            n.date_update AS fechamento,
            DATEDIFF(n.date_update, n.date_create) AS dias
        FROM crm_negocio n
        LEFT JOIN users u ON n.id_user = u.id_users
        WHERE (n.origem IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE') 
               OR n.canal IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE'))
          AND n.id_state = 6
          AND n.date_create >= %s AND n.date_create <= %s
        ORDER BY n.date_update DESC
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (start, end))
            return cursor.fetchall()
    finally:
        conn.close()


def get_vendas_midia_detalhadas(ano: int, mes: int) -> list:
    """Busca vendas detalhadas de mídia paga"""
    conn = get_crm_connection()
    try:
        query = """
        SELECT 
            n.id_crm_negocio AS id,
            n.origem,
            n.canal,
            CASE 
                WHEN n.origem = 'INSTAGRAM' OR n.canal = 'INSTAGRAM' THEN 'INSTAGRAM'
                WHEN n.origem = 'FACEBOOK' OR n.canal = 'FACEBOOK' THEN 'FACEBOOK'
                WHEN n.origem = 'GOOGLE' OR n.canal = 'GOOGLE' THEN 'GOOGLE'
            END AS plataforma,
            n.titulo AS veiculo,
            n.cliente,
            u.name AS vendedor,
            n.valor,
            n.date_create AS entrada,
            n.date_update AS fechamento,
            DATEDIFF(n.date_update, n.date_create) AS dias
        FROM crm_negocio n
        LEFT JOIN users u ON n.id_user = u.id_users
        WHERE (n.origem IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE') 
               OR n.canal IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE'))
          AND n.id_state = 6
          AND YEAR(n.date_create) = %s AND MONTH(n.date_create) = %s
        ORDER BY n.date_update DESC
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (ano, mes))
            return cursor.fetchall()
    finally:
        conn.close()


def get_resumo_por_vendedor_midia(ano: int, mes: int) -> list:
    """Busca resumo por vendedor (apenas leads de mídia paga)"""
    conn = get_crm_connection()
    try:
        query = """
        SELECT 
            u.name AS vendedor,
            COUNT(*) AS total_leads,
            SUM(CASE WHEN n.id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN n.id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
            SUM(CASE WHEN n.id_state = 6 THEN n.valor ELSE 0 END) AS valor_vendido
        FROM crm_negocio n
        LEFT JOIN users u ON n.id_user = u.id_users
        WHERE (n.origem IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE') 
               OR n.canal IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE'))
          AND YEAR(n.date_create) = %s AND MONTH(n.date_create) = %s
        GROUP BY n.id_user, u.name
        ORDER BY ganhos DESC
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (ano, mes))
            results = cursor.fetchall()
        
        for r in results:
            ganhos = r['ganhos'] or 0
            perdidos = r['perdidos'] or 0
            total = ganhos + perdidos
            r['taxa_conversao'] = round((ganhos / total * 100) if total > 0 else 0, 2)
            r['valor_vendido'] = float(r['valor_vendido'] or 0)
        
        return results
    finally:
        conn.close()


def get_motivos_perda_midia(ano: int, mes: int) -> list:
    """Busca motivos de perda de leads de mídia paga"""
    conn = get_crm_connection()
    try:
        query = """
        SELECT 
            COALESCE(motivo_perda, 'NÃO INFORMADO') AS motivo,
            COUNT(*) AS quantidade
        FROM crm_negocio
        WHERE (origem IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE') 
               OR canal IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE'))
          AND id_state = 7
          AND YEAR(date_create) = %s AND MONTH(date_create) = %s
        GROUP BY motivo_perda
        ORDER BY quantidade DESC
        LIMIT 10
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (ano, mes))
            results = cursor.fetchall()
        
        total = sum(r['quantidade'] for r in results)
        for r in results:
            r['percentual'] = round((r['quantidade'] / total * 100) if total > 0 else 0, 1)
        
        return results
    finally:
        conn.close()


def get_resumo_por_origem(ano: int, mes: int) -> list:
    """Busca resumo por origem agrupada (todas as origens)"""
    conn = get_crm_connection()
    try:
        query = """
        SELECT 
            CASE 
                WHEN origem = 'INSTAGRAM' OR canal = 'INSTAGRAM' THEN 'INSTAGRAM'
                WHEN origem = 'FACEBOOK' OR canal = 'FACEBOOK' THEN 'FACEBOOK'
                WHEN origem = 'GOOGLE' OR canal = 'GOOGLE' THEN 'GOOGLE'
                WHEN origem = 'SITE' THEN 'SITE'
                WHEN origem IN ('WEBMOTORS', 'ICARROS', 'MEUCARRONOVO', 'MERCADO LIVRE', 'MOBIAUTO', 'AUTOLINE', 'POACARROS', 'SOCARRAO', 'Autocarro', 'AUTOCARRO') THEN 'PORTAIS'
                WHEN origem IN ('SHOWROOM', 'NA PISTA', 'FEIRÃO') AND canal NOT IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE') THEN 'PRESENCIAL'
                WHEN origem IN ('WHATSAPP', 'TELEFONE', 'TELEMARKETING') THEN 'DIRETO'
                WHEN origem IN ('INDICACAO', 'INDICAÇÃO CAMPANHA', 'REDE RELACIONAMENTO') THEN 'INDICACAO'
                ELSE 'OUTROS'
            END AS grupo_origem,
            COUNT(*) AS total_leads,
            SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
            SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) AS valor_vendido
        FROM crm_negocio
        WHERE YEAR(date_create) = %s AND MONTH(date_create) = %s
        GROUP BY grupo_origem
        ORDER BY ganhos DESC
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (ano, mes))
            results = cursor.fetchall()
        
        for r in results:
            ganhos = r['ganhos'] or 0
            perdidos = r['perdidos'] or 0
            total = ganhos + perdidos
            r['taxa_conversao'] = round((ganhos / total * 100) if total > 0 else 0, 2)
            r['valor_vendido'] = float(r['valor_vendido'] or 0)
        
        return results
    finally:
        conn.close()


def get_resumo_por_vendedor(ano: int, mes: int) -> list:
    """Busca resumo por vendedor (todas as origens)"""
    conn = get_crm_connection()
    try:
        query = """
        SELECT 
            u.name AS vendedor,
            COUNT(*) AS total_leads,
            SUM(CASE WHEN n.id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN n.id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
            SUM(CASE WHEN n.id_state = 6 THEN n.valor ELSE 0 END) AS valor_vendido
        FROM crm_negocio n
        LEFT JOIN users u ON n.id_user = u.id_users
        WHERE YEAR(n.date_create) = %s AND MONTH(n.date_create) = %s
        GROUP BY n.id_user, u.name
        ORDER BY ganhos DESC
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (ano, mes))
            results = cursor.fetchall()
        
        for r in results:
            ganhos = r['ganhos'] or 0
            perdidos = r['perdidos'] or 0
            total = ganhos + perdidos
            r['taxa_conversao'] = round((ganhos / total * 100) if total > 0 else 0, 2)
            r['valor_vendido'] = float(r['valor_vendido'] or 0)
        
        return results
    finally:
        conn.close()


def get_motivos_perda(ano: int, mes: int) -> list:
    """Busca top motivos de perda (todas as origens)"""
    conn = get_crm_connection()
    try:
        query = """
        SELECT 
            COALESCE(motivo_perda, 'NÃO INFORMADO') AS motivo_perda,
            COUNT(*) AS quantidade
        FROM crm_negocio
        WHERE id_state = 7
          AND motivo_perda IS NOT NULL
          AND motivo_perda != ''
          AND YEAR(date_create) = %s AND MONTH(date_create) = %s
        GROUP BY motivo_perda
        ORDER BY quantidade DESC
        LIMIT 10
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (ano, mes))
            results = cursor.fetchall()
        
        total = sum(r['quantidade'] for r in results)
        for r in results:
            r['percentual'] = round((r['quantidade'] / total * 100) if total > 0 else 0, 1)
        
        return results
    finally:
        conn.close()


@app.get("/")
async def root():
    return {"message": "ROI Dashboard API v2.0", "docs": "/docs", "nota": "Considera origem E canal como fonte de mídia"}


@app.get("/health")
async def health():
    try:
        conn = get_crm_connection()
        conn.close()
        return {"status": "healthy", "crm": "connected", "version": "2.0"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.get("/api/roi/dashboard/{ano}/{mes}")
async def get_dashboard(ano: int, mes: int):
    """
    Dashboard principal de cruzamento CRM vs Agência
    CORRIGIDO: Considera origem OU canal como fonte de mídia paga
    """
    
    periodo_key = f"{ano}-{mes:02d}"
    agencia = AGENCY_DATA.get(periodo_key, {})
    
    if not agencia:
        # Usar estimativa se não tiver dados
        agencia = {
            "investimento_meta": 8500,
            "investimento_google": 7000,
            "investimento_total": 15500,
            "total_leads_reportados": 0
        }
    
    try:
        # Buscar dados reais do CRM
        resumo_mes = get_resumo_mes(ano, mes)
        resumo_midia = get_resumo_midia_paga(ano, mes)
        resumo_origem = get_resumo_por_origem(ano, mes)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar CRM: {str(e)}")
    
    # Dados do CRM
    leads_crm_total = resumo_mes.get('total_leads', 0)
    vendas_crm = resumo_mes.get('ganhos', 0)
    valor_vendido = resumo_mes.get('valor_vendido', 0)
    
    # Dados de mídia paga (Instagram + Facebook + Google)
    insta = resumo_midia.get('INSTAGRAM', {})
    fb = resumo_midia.get('FACEBOOK', {})
    google = resumo_midia.get('GOOGLE', {})
    
    # META = Instagram + Facebook
    leads_meta = int(insta.get('leads', 0) or 0) + int(fb.get('leads', 0) or 0)
    vendas_meta = int(insta.get('vendas', 0) or 0) + int(fb.get('vendas', 0) or 0)
    valor_meta = float(insta.get('valor', 0) or 0) + float(fb.get('valor', 0) or 0)
    
    # GOOGLE
    leads_google = int(google.get('leads', 0) or 0)
    vendas_google = int(google.get('vendas', 0) or 0)
    valor_google = float(google.get('valor', 0) or 0)
    
    # Total mídia paga
    leads_midia = leads_meta + leads_google
    vendas_midia = vendas_meta + vendas_google
    valor_midia = float(valor_meta) + float(valor_google)
    
    # Dados da agência
    investimento_total = agencia.get('investimento_total', 15500)
    investimento_meta = agencia.get('investimento_meta', 8500)
    investimento_google = agencia.get('investimento_google', 7000)
    leads_agencia = agencia.get('total_leads_reportados', 0)
    
    # Cálculos de ROI
    cpl_agencia = investimento_total / leads_agencia if leads_agencia > 0 else 0
    cpl_real = investimento_total / leads_midia if leads_midia > 0 else 0
    cpv = investimento_total / vendas_midia if vendas_midia > 0 else 0
    roi = (valor_midia / investimento_total * 100) if investimento_total > 0 else 0
    
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
    
    if leads_agencia > 0 and leads_midia > 0:
        diferenca = leads_agencia - leads_midia
        if diferenca > 50:
            alertas.append(f"⚠️ Agência reporta {diferenca} leads a mais que o CRM")
    
    if vendas_meta <= 2 and investimento_meta > 5000:
        alertas.append(f"🔴 META: R$ {investimento_meta:,.0f} investidos, apenas {vendas_meta} vendas")
    
    if vendas_google == 0 and investimento_google > 5000:
        alertas.append(f"🔴 GOOGLE: R$ {investimento_google:,.0f} investidos, {vendas_google} vendas")
    
    taxa = resumo_mes.get('taxa_conversao', 0)
    if taxa < 10:
        alertas.append(f"📉 Taxa de conversão geral baixa: {taxa:.1f}%")
    
    # Gerar insights
    insights = []
    
    # Melhor canal
    indicacao = next((r for r in resumo_origem if r.get('grupo_origem') == 'INDICACAO'), {})
    if indicacao.get('ganhos', 0) > 0:
        insights.append(f"🏆 INDICAÇÃO: {indicacao.get('ganhos', 0)} vendas ({indicacao.get('taxa_conversao', 0)}% conversão) - custo zero!")
    
    if roi_google > roi_meta and vendas_google > 0:
        insights.append(f"💡 Google ROI ({roi_google:.0f}%) superior ao Meta ({roi_meta:.0f}%)")
    elif roi_meta > roi_google and vendas_meta > 0:
        insights.append(f"💡 Meta ROI ({roi_meta:.0f}%) superior ao Google ({roi_google:.0f}%)")
    
    if vendas_midia > 0:
        ticket = valor_midia / vendas_midia
        insights.append(f"🎯 Ticket médio mídia paga: R$ {ticket:,.0f}")
    
    if indicacao.get('taxa_conversao', 0) > 40:
        insights.append(f"⭐ Indicação tem {indicacao.get('taxa_conversao', 0)}% de conversão - investir em programa de indicação!")
    
    return {
        "periodo": f"{mes:02d}/{ano}",
        "investimento_total": investimento_total,
        "leads_agencia": leads_agencia,
        "leads_crm": leads_midia,  # Leads de mídia paga no CRM
        "leads_crm_total": leads_crm_total,  # Total de leads
        "vendas_crm": vendas_midia,  # Vendas de mídia paga
        "vendas_crm_total": vendas_crm,  # Total de vendas
        "valor_vendido": valor_midia,  # Valor de mídia paga
        "valor_vendido_total": valor_vendido,  # Valor total
        "custo_por_lead_agencia": round(cpl_agencia, 2),
        "custo_por_lead_real": round(cpl_real, 2),
        "custo_por_venda": round(cpv, 2),
        "roi_percentual": round(roi, 2),
        "meta": {
            "investimento": investimento_meta,
            "leads_agencia": agencia.get('meta_conversoes', 0),
            "leads_crm": leads_meta,
            "leads_instagram": insta.get('leads', 0),
            "leads_facebook": fb.get('leads', 0),
            "vendas": vendas_meta,
            "vendas_instagram": insta.get('vendas', 0),
            "vendas_facebook": fb.get('vendas', 0),
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
            "leads_midia": leads_midia,
            "em_andamento": resumo_mes.get('em_andamento', 0),
            "ganhos": vendas_crm,
            "ganhos_midia": vendas_midia,
            "perdidos": resumo_mes.get('perdidos', 0),
            "taxa_conversao": resumo_mes.get('taxa_conversao', 0)
        },
        "alertas": alertas,
        "insights": insights
    }


@app.get("/api/roi/vendas/{ano}/{mes}")
async def get_vendas_detalhadas(ano: int, mes: int):
    """Lista vendas detalhadas de mídia paga do mês"""
    try:
        vendas = get_vendas_midia_detalhadas(ano, mes)
        
        resultado = []
        for v in vendas:
            resultado.append({
                "id": v['id'],
                "plataforma": v['plataforma'],
                "origem": v['origem'],
                "canal": v['canal'],
                "veiculo": v['veiculo'],
                "cliente": v['cliente'],
                "vendedor": v['vendedor'],
                "valor": float(v['valor'] or 0),
                "dias": v['dias'],
                "entrada": str(v['entrada']),
                "fechamento": str(v['fechamento'])
            })
        
        total = sum(r['valor'] for r in resultado)
        
        return {
            "periodo": f"{mes:02d}/{ano}",
            "total_vendas": len(resultado),
            "valor_total": total,
            "vendas": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/roi/insights/{ano}/{mes}")
async def get_insights(ano: int, mes: int):
    """Insights detalhados e recomendações"""
    
    periodo_key = f"{ano}-{mes:02d}"
    agencia = AGENCY_DATA.get(periodo_key, {})
    
    try:
        resumo_midia = get_resumo_midia_paga(ano, mes)
        resumo_vendedor = get_resumo_por_vendedor_midia(ano, mes)
        motivos_perda = get_motivos_perda_midia(ano, mes)
        resumo_origem = get_resumo_por_origem(ano, mes)
        resumo_mes = get_resumo_mes(ano, mes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    insights = []
    recomendacoes = []
    
    # Dados
    insta = resumo_midia.get('INSTAGRAM', {})
    fb = resumo_midia.get('FACEBOOK', {})
    google = resumo_midia.get('GOOGLE', {})
    
    inv_meta = agencia.get('investimento_meta', 8500)
    inv_google = agencia.get('investimento_google', 7000)
    
    vendas_meta = insta.get('vendas', 0) + fb.get('vendas', 0)
    vendas_google = google.get('vendas', 0)
    
    # Análise META
    if inv_meta > 0:
        cpv_meta = inv_meta / vendas_meta if vendas_meta > 0 else float('inf')
        if vendas_meta <= 2:
            insights.append({
                "tipo": "alerta",
                "titulo": "META com baixo retorno",
                "descricao": f"R$ {inv_meta:,.0f} investidos geraram apenas {vendas_meta} vendas",
                "impacto": f"Custo por venda: R$ {cpv_meta:,.0f}" if vendas_meta > 0 else "Sem vendas"
            })
            recomendacoes.append({
                "acao": "Revisar segmentação e criativos das campanhas META",
                "expectativa": "Aumentar conversão de leads em vendas",
                "prioridade": "alta"
            })
    
    # Análise GOOGLE
    if inv_google > 0 and vendas_google == 0:
        insights.append({
            "tipo": "alerta",
            "titulo": "GOOGLE sem vendas",
            "descricao": f"R$ {inv_google:,.0f} investidos sem vendas atribuídas",
            "impacto": "Verificar rastreamento de UTMs"
        })
        recomendacoes.append({
            "acao": "Auditar UTMs e verificar se leads chegam com origem correta",
            "expectativa": "Identificar vendas que podem estar sem atribuição",
            "prioridade": "alta"
        })
    
    # Análise de vendedores
    if resumo_vendedor:
        vendedores_com_vendas = [v for v in resumo_vendedor if v.get('ganhos', 0) > 0]
        if vendedores_com_vendas:
            melhor = max(vendedores_com_vendas, key=lambda x: x.get('taxa_conversao', 0))
            insights.append({
                "tipo": "oportunidade",
                "titulo": f"{melhor['vendedor']} é o melhor em mídia paga",
                "descricao": f"{melhor['ganhos']} vendas com {melhor['taxa_conversao']}% de conversão",
                "impacto": "Replicar metodologia para o time"
            })
            recomendacoes.append({
                "acao": f"Treinar equipe com a metodologia de {melhor['vendedor']}",
                "expectativa": "Aumentar conversão geral do time",
                "prioridade": "media"
            })
    
    # Análise de motivos de perda
    if motivos_perda:
        nao_responde = sum(m['quantidade'] for m in motivos_perda if 'responde' in m['motivo'].lower())
        if nao_responde > 20:
            insights.append({
                "tipo": "alerta",
                "titulo": f"{nao_responde} leads não respondem",
                "descricao": "Leads frios ou tempo de resposta lento",
                "impacto": "Implementar resposta em menos de 5 minutos"
            })
            recomendacoes.append({
                "acao": "Configurar alerta de lead novo para resposta imediata",
                "expectativa": "Reduzir 'não responde' em 50%",
                "prioridade": "alta"
            })
    
    # Análise de INDICAÇÃO
    indicacao = next((r for r in resumo_origem if r.get('grupo_origem') == 'INDICACAO'), {})
    if indicacao.get('taxa_conversao', 0) > 30:
        insights.append({
            "tipo": "oportunidade",
            "titulo": "Indicação é o melhor canal",
            "descricao": f"{indicacao.get('ganhos', 0)} vendas com {indicacao.get('taxa_conversao', 0)}% de conversão",
            "impacto": "Custo zero de mídia!"
        })
        recomendacoes.append({
            "acao": "Criar programa de indicação com bonificação",
            "expectativa": "Dobrar vendas por indicação em 3 meses",
            "prioridade": "alta"
        })
    
    return {
        "periodo": f"{mes:02d}/{ano}",
        "insights": insights,
        "recomendacoes": recomendacoes,
        "dados": {
            "por_plataforma": {
                "instagram": insta,
                "facebook": fb,
                "google": google
            },
            "por_vendedor": resumo_vendedor,
            "motivos_perda": motivos_perda,
            "por_origem": resumo_origem,
            "resumo_mes": resumo_mes
        }
    }


@app.get("/api/roi/agencia/reports")
async def list_agency_reports():
    """Lista relatórios da agência disponíveis"""
    return {
        "reports": [
            {"periodo": k, **v} for k, v in sorted(AGENCY_DATA.items(), reverse=True)
        ]
    }


@app.get("/api/roi/comparativo")
async def get_comparativo_periodo():
    """Comparativo dos últimos meses"""
    
    meses = [
        (2025, 10), (2025, 11), (2025, 12), (2026, 1)
    ]
    
    resultados = []
    
    for ano, mes in meses:
        try:
            periodo_key = f"{ano}-{mes:02d}"
            agencia = AGENCY_DATA.get(periodo_key, {})
            
            resumo_midia = get_resumo_midia_paga(ano, mes)
            
            insta = resumo_midia.get('INSTAGRAM', {})
            fb = resumo_midia.get('FACEBOOK', {})
            google = resumo_midia.get('GOOGLE', {})
            
            vendas = insta.get('vendas', 0) + fb.get('vendas', 0) + google.get('vendas', 0)
            valor = insta.get('valor', 0) + fb.get('valor', 0) + google.get('valor', 0)
            leads = insta.get('leads', 0) + fb.get('leads', 0) + google.get('leads', 0)
            
            investimento = agencia.get('investimento_total', 0)
            
            resultados.append({
                "periodo": f"{mes:02d}/{ano}",
                "ano": ano,
                "mes": mes,
                "investimento": investimento,
                "leads": leads,
                "vendas": vendas,
                "valor": valor,
                "custo_por_venda": investimento / vendas if vendas > 0 else 0,
                "roi": (valor / investimento * 100) if investimento > 0 else 0
            })
        except Exception:
            pass
    
    return {"periodos": resultados}


@app.get("/api/roi/consolidado")
async def get_consolidado(
    start: str = "2025-10-01",
    end: str = "2026-01-14",
):
    """
    Retorna o consolidado do período (por date_create no CRM).
    Default: 01/10/2025 a 14/01/2026.
    """
    try:
        start_d = _parse_ymd(start)
        end_d = _parse_ymd(end)
        if end_d < start_d:
            raise HTTPException(status_code=400, detail="end deve ser >= start")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD.")

    # CRM (período)
    resumo_mes = get_resumo_mes_range(start_d, end_d)
    resumo_midia = get_resumo_midia_paga_range(start_d, end_d)

    # Agência (soma pró-rateada do período)
    agencia_sum = _agency_sum_for_range(start_d, end_d)

    # CRM totals
    leads_crm_total = resumo_mes.get("total_leads", 0)
    vendas_crm_total = resumo_mes.get("ganhos", 0)
    valor_vendido_total = resumo_mes.get("valor_vendido", 0.0)

    insta = resumo_midia.get("INSTAGRAM", {})
    fb = resumo_midia.get("FACEBOOK", {})
    google = resumo_midia.get("GOOGLE", {})

    # META = Instagram + Facebook
    leads_meta = int(insta.get("leads", 0) or 0) + int(fb.get("leads", 0) or 0)
    vendas_meta = int(insta.get("vendas", 0) or 0) + int(fb.get("vendas", 0) or 0)
    valor_meta = float(insta.get("valor", 0) or 0) + float(fb.get("valor", 0) or 0)

    leads_google = int(google.get("leads", 0) or 0)
    vendas_google = int(google.get("vendas", 0) or 0)
    valor_google = float(google.get("valor", 0) or 0)

    leads_midia = leads_meta + leads_google
    vendas_midia = vendas_meta + vendas_google
    valor_midia = float(valor_meta) + float(valor_google)

    investimento_total = float(agencia_sum.get("investimento_total", 0.0) or 0.0)
    investimento_meta = float(agencia_sum.get("investimento_meta", 0.0) or 0.0)
    investimento_google = float(agencia_sum.get("investimento_google", 0.0) or 0.0)
    leads_agencia = float(agencia_sum.get("leads_reportados", 0.0) or 0.0)

    # Cálculos
    cpl_agencia = investimento_total / leads_agencia if leads_agencia > 0 else 0
    cpl_real = investimento_total / leads_midia if leads_midia > 0 else 0
    cpv = investimento_total / vendas_midia if vendas_midia > 0 else 0
    roi = (valor_midia / investimento_total * 100) if investimento_total > 0 else 0

    cpl_meta = investimento_meta / leads_meta if leads_meta > 0 else 0
    cpv_meta = investimento_meta / vendas_meta if vendas_meta > 0 else 0
    roi_meta = (valor_meta / investimento_meta * 100) if investimento_meta > 0 else 0

    cpl_google = investimento_google / leads_google if leads_google > 0 else 0
    cpv_google = investimento_google / vendas_google if vendas_google > 0 else 0
    roi_google = (valor_google / investimento_google * 100) if investimento_google > 0 else 0

    # Alertas e insights (foco em clareza do período)
    alertas = []
    insights = []

    if leads_agencia > 0 and leads_midia > 0:
        diferenca = leads_agencia - leads_midia
        if diferenca > 50:
            alertas.append(f"⚠️ Agência reporta ~{int(diferenca)} leads a mais que o CRM no período")

    insights.append(f"📅 Período apurado (entrada no CRM - date_create): {start_d.strftime('%d/%m/%Y')} a {end_d.strftime('%d/%m/%Y')}")

    if vendas_midia > 0:
        ticket = valor_midia / float(vendas_midia)
        insights.append(f"🎯 Ticket médio mídia paga no período: R$ {ticket:,.0f}")

    if roi_google > roi_meta and vendas_google > 0:
        insights.append(f"💡 Google ROI ({roi_google:.0f}%) superior ao Meta ({roi_meta:.0f}%) no período")
    elif roi_meta > roi_google and vendas_meta > 0:
        insights.append(f"💡 Meta ROI ({roi_meta:.0f}%) superior ao Google ({roi_google:.0f}%) no período")

    return {
        "periodo": f"{start_d.strftime('%d/%m/%Y')} a {end_d.strftime('%d/%m/%Y')}",
        "periodo_inicio": start_d.strftime("%Y-%m-%d"),
        "periodo_fim": end_d.strftime("%Y-%m-%d"),
        "investimento_total": round(investimento_total, 2),
        "leads_agencia": int(leads_agencia),
        "leads_crm": leads_midia,
        "leads_crm_total": leads_crm_total,
        "vendas_crm": vendas_midia,
        "vendas_crm_total": vendas_crm_total,
        "valor_vendido": valor_midia,
        "valor_vendido_total": valor_vendido_total,
        "custo_por_lead_agencia": round(cpl_agencia, 2),
        "custo_por_lead_real": round(cpl_real, 2),
        "custo_por_venda": round(cpv, 2),
        "roi_percentual": round(roi, 2),
        "meta": {
            "investimento": round(investimento_meta, 2),
            "leads_agencia": int(agencia_sum.get("meta_leads_reportados", 0.0) or 0.0),
            "leads_crm": leads_meta,
            "leads_instagram": int(insta.get("leads", 0) or 0),
            "leads_facebook": int(fb.get("leads", 0) or 0),
            "vendas": vendas_meta,
            "vendas_instagram": int(insta.get("vendas", 0) or 0),
            "vendas_facebook": int(fb.get("vendas", 0) or 0),
            "valor_vendido": valor_meta,
            "custo_por_lead": round(cpl_meta, 2),
            "custo_por_venda": round(cpv_meta, 2),
            "roi": round(roi_meta, 2),
            "alcance": int(agencia_sum.get("meta_alcance", 0.0) or 0.0),
            "cliques": int(agencia_sum.get("meta_cliques", 0.0) or 0.0),
        },
        "google": {
            "investimento": round(investimento_google, 2),
            "leads_agencia": int(agencia_sum.get("google_leads_reportados", 0.0) or 0.0),
            "leads_crm": leads_google,
            "vendas": vendas_google,
            "valor_vendido": valor_google,
            "custo_por_lead": round(cpl_google, 2),
            "custo_por_venda": round(cpv_google, 2),
            "roi": round(roi_google, 2),
            "cliques": int(agencia_sum.get("google_cliques", 0.0) or 0.0),
            "whatsapp": int(agencia_sum.get("google_whatsapp", 0.0) or 0.0),
        },
        "funil": {
            "leads_total": leads_crm_total,
            "leads_midia": leads_midia,
            "em_andamento": resumo_mes.get("em_andamento", 0),
            "ganhos": vendas_crm_total,
            "ganhos_midia": vendas_midia,
            "perdidos": resumo_mes.get("perdidos", 0),
            "taxa_conversao": resumo_mes.get("taxa_conversao", 0),
        },
        "alertas": alertas,
        "insights": insights,
        "observacao_agencia": "Investimento/leads da agência são somados por mês e pró-rateados no período selecionado (quando parcial).",
    }


@app.get("/api/roi/vendas/consolidado")
async def get_vendas_consolidado(
    start: str = "2025-10-01",
    end: str = "2026-01-14",
):
    """Lista vendas detalhadas de mídia paga no consolidado (origem OU canal)."""
    try:
        start_d = _parse_ymd(start)
        end_d = _parse_ymd(end)
        if end_d < start_d:
            raise HTTPException(status_code=400, detail="end deve ser >= start")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD.")

    vendas = get_vendas_midia_range(start_d, end_d)
    resultado = []
    for v in vendas:
        resultado.append({
            "id": v["id"],
            "plataforma": v["plataforma"],
            "origem": v["origem"],
            "canal": v["canal"],
            "veiculo": v["veiculo"],
            "cliente": v["cliente"],
            "vendedor": v["vendedor"],
            "valor": float(v["valor"] or 0),
            "dias": v["dias"],
            "entrada": str(v["entrada"]),
            "fechamento": str(v["fechamento"]),
        })

    total = sum(r["valor"] for r in resultado)
    return {
        "periodo": f"{start_d.strftime('%d/%m/%Y')} a {end_d.strftime('%d/%m/%Y')}",
        "total_vendas": len(resultado),
        "valor_total": total,
        "vendas": resultado,
    }


@app.get("/api/roi/qualidade-leads")
async def get_qualidade_leads():
    """Análise de qualidade dos leads - para apresentação"""
    
    conn = get_crm_connection()
    try:
        # 1. Comparativo por origem
        query_origens = """
        SELECT 
            CASE 
                WHEN origem = 'INSTAGRAM' OR canal = 'INSTAGRAM' THEN 'INSTAGRAM'
                WHEN origem = 'FACEBOOK' OR canal = 'FACEBOOK' THEN 'FACEBOOK'
                WHEN origem = 'GOOGLE' OR canal = 'GOOGLE' THEN 'GOOGLE'
                WHEN origem IN ('INDICACAO', 'INDICAÇÃO CAMPANHA', 'REDE RELACIONAMENTO') THEN 'INDICAÇÃO'
                WHEN origem IN ('SHOWROOM', 'NA PISTA', 'FEIRÃO') AND canal NOT IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE') THEN 'SHOWROOM'
                WHEN origem IN ('WEBMOTORS', 'ICARROS', 'MEUCARRONOVO', 'MERCADO LIVRE', 'MOBIAUTO') THEN 'PORTAIS'
                ELSE 'OUTROS'
            END AS fonte,
            COUNT(*) AS total_leads,
            SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
            SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) AS valor_vendido
        FROM crm_negocio
        WHERE date_create >= '2025-10-01' AND date_create <= '2026-01-14'
        GROUP BY fonte
        ORDER BY total_leads DESC
        """
        
        with conn.cursor() as cursor:
            cursor.execute(query_origens)
            origens_raw = cursor.fetchall()
        
        origens = []
        for o in origens_raw:
            ganhos = int(o['ganhos'] or 0)
            perdidos = int(o['perdidos'] or 0)
            total = ganhos + perdidos
            taxa = round((ganhos / total * 100), 1) if total > 0 else 0
            origens.append({
                "fonte": o['fonte'],
                "total_leads": o['total_leads'],
                "ganhos": ganhos,
                "perdidos": perdidos,
                "taxa_conversao": taxa,
                "valor_vendido": float(o['valor_vendido'] or 0),
                "qualidade": "alta" if taxa >= 30 else "media" if taxa >= 10 else "baixa"
            })
        
        # 2. Resumo mídia paga
        query_midia = """
        SELECT 
            COUNT(*) AS total_leads,
            SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
            SUM(CASE WHEN id_state BETWEEN 1 AND 5 THEN 1 ELSE 0 END) AS em_andamento
        FROM crm_negocio
        WHERE (origem IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE') 
               OR canal IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE'))
          AND date_create >= '2025-10-01' AND date_create <= '2026-01-14'
        """
        
        with conn.cursor() as cursor:
            cursor.execute(query_midia)
            midia = cursor.fetchone()
        
        total_midia = int(midia['total_leads'] or 0)
        ganhos_midia = int(midia['ganhos'] or 0)
        perdidos_midia = int(midia['perdidos'] or 0)
        taxa_midia = round((ganhos_midia / (ganhos_midia + perdidos_midia) * 100), 1) if (ganhos_midia + perdidos_midia) > 0 else 0
        
        # 3. Motivos de perda
        query_motivos = """
        SELECT 
            COALESCE(NULLIF(motivo_perda, ''), 'NÃO INFORMADO') AS motivo,
            COUNT(*) AS quantidade
        FROM crm_negocio
        WHERE (origem IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE') 
               OR canal IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE'))
          AND id_state = 7
          AND date_create >= '2025-10-01' AND date_create <= '2026-01-14'
        GROUP BY motivo_perda
        ORDER BY quantidade DESC
        LIMIT 10
        """
        
        with conn.cursor() as cursor:
            cursor.execute(query_motivos)
            motivos_raw = cursor.fetchall()
        
        total_perdidos_motivos = sum(m['quantidade'] for m in motivos_raw)
        motivos = []
        for m in motivos_raw:
            pct = round((m['quantidade'] / total_perdidos_motivos * 100), 1) if total_perdidos_motivos > 0 else 0
            motivos.append({
                "motivo": m['motivo'],
                "quantidade": m['quantidade'],
                "percentual": pct
            })
        
        # 4. Indicação para comparativo
        query_indicacao = """
        SELECT 
            COUNT(*) AS total,
            SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos
        FROM crm_negocio
        WHERE origem IN ('INDICACAO', 'INDICAÇÃO CAMPANHA', 'REDE RELACIONAMENTO')
          AND date_create >= '2025-10-01' AND date_create <= '2026-01-14'
        """
        
        with conn.cursor() as cursor:
            cursor.execute(query_indicacao)
            ind = cursor.fetchone()
        
        ganhos_ind = int(ind['ganhos'] or 0)
        perdidos_ind = int(ind['perdidos'] or 0)
        taxa_ind = round((ganhos_ind / (ganhos_ind + perdidos_ind) * 100), 1) if (ganhos_ind + perdidos_ind) > 0 else 0
        
        # 5. Vendedores
        query_vendedores = """
        SELECT 
            u.name AS vendedor,
            COUNT(*) AS total_leads,
            SUM(CASE WHEN n.id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN n.id_state = 7 THEN 1 ELSE 0 END) AS perdidos
        FROM crm_negocio n
        LEFT JOIN users u ON n.id_user = u.id_users
        WHERE (n.origem IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE') 
               OR n.canal IN ('INSTAGRAM', 'FACEBOOK', 'GOOGLE'))
          AND n.date_create >= '2025-10-01' AND n.date_create <= '2026-01-14'
        GROUP BY n.id_user, u.name
        HAVING total_leads >= 10
        ORDER BY ganhos DESC
        """
        
        with conn.cursor() as cursor:
            cursor.execute(query_vendedores)
            vendedores_raw = cursor.fetchall()
        
        vendedores = []
        for v in vendedores_raw:
            ganhos_v = int(v['ganhos'] or 0)
            perdidos_v = int(v['perdidos'] or 0)
            total_v = ganhos_v + perdidos_v
            taxa_v = round((ganhos_v / total_v * 100), 1) if total_v > 0 else 0
            vendedores.append({
                "vendedor": v['vendedor'] or 'N/A',
                "total_leads": v['total_leads'],
                "ganhos": ganhos_v,
                "perdidos": perdidos_v,
                "taxa_conversao": taxa_v
            })
        
        # Cálculos de custo
        investimento = 62098
        custo_por_lead = round(investimento / total_midia, 2) if total_midia > 0 else 0
        custo_por_venda = round(investimento / ganhos_midia, 2) if ganhos_midia > 0 else 0
        leads_frios_pct = round(((motivos[0]['quantidade'] + motivos[1]['quantidade']) / total_perdidos_motivos * 100), 1) if len(motivos) >= 2 else 0
        
        multiplicador = round(taxa_ind / taxa_midia, 1) if taxa_midia > 0 else 0
        
        return {
            "periodo": "01/10/2025 a 14/01/2026",
            "investimento_total": investimento,
            "resumo_midia": {
                "total_leads": total_midia,
                "ganhos": ganhos_midia,
                "perdidos": perdidos_midia,
                "em_andamento": int(midia['em_andamento'] or 0),
                "taxa_conversao": taxa_midia,
                "custo_por_lead": custo_por_lead,
                "custo_por_venda": custo_por_venda
            },
            "comparativo_indicacao": {
                "total_leads": int(ind['total'] or 0),
                "ganhos": ganhos_ind,
                "perdidos": perdidos_ind,
                "taxa_conversao": taxa_ind,
                "custo": 0,
                "multiplicador": multiplicador
            },
            "origens": origens,
            "motivos_perda": motivos,
            "leads_frios_percentual": leads_frios_pct,
            "vendedores": vendedores,
            "alertas": [
                f"🔴 Taxa de conversão mídia paga: apenas {taxa_midia}%",
                f"🔴 {perdidos_midia} leads trabalhados sem resultado",
                f"🔴 {leads_frios_pct}% dos perdidos são leads frios (sem interesse/não responde)",
                f"🟢 Indicação converte {multiplicador}x mais que mídia paga"
            ],
            "recomendacoes": [
                {
                    "acao": "Questionar a agência sobre segmentação",
                    "motivo": f"{leads_frios_pct}% dos leads são frios",
                    "prioridade": "alta"
                },
                {
                    "acao": "Criar programa de indicação com bonificação",
                    "motivo": f"Indicação converte {multiplicador}x mais com custo zero",
                    "prioridade": "alta"
                },
                {
                    "acao": "Contratar SDR para filtrar leads",
                    "motivo": "Vendedores perdem tempo com leads frios",
                    "prioridade": "media"
                },
                {
                    "acao": "Responder leads em menos de 5 minutos",
                    "motivo": f"{motivos[1]['quantidade'] if len(motivos) > 1 else 0} leads não responderam",
                    "prioridade": "alta"
                }
            ]
        }
    finally:
        conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
