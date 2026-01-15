"""
Task Celery para sincronização periódica do CRM externo
"""
import os
from datetime import date, timedelta
import structlog
import pymysql
from pymysql.cursors import DictCursor

from celery_app import celery_app

logger = structlog.get_logger()


def get_external_connection():
    """Conecta ao CRM externo MySQL"""
    return pymysql.connect(
        host=os.getenv("EXTERNAL_CRM_HOST", "mysql.netcar-rc.com.br"),
        port=int(os.getenv("EXTERNAL_CRM_PORT", "3306")),
        database=os.getenv("EXTERNAL_CRM_DATABASE", "netcarrc01"),
        user=os.getenv("EXTERNAL_CRM_USER", ""),
        password=os.getenv("EXTERNAL_CRM_PASSWORD", ""),
        cursorclass=DictCursor,
        charset='utf8mb4',
        connect_timeout=10,
        read_timeout=30
    )


@celery_app.task(name="sync_crm_external")
def sync_crm_external(dias: int = 1):
    """
    Sincroniza dados do CRM externo
    
    Executa a cada 5 minutos via Celery Beat
    Por padrão, busca apenas o último dia (incremental)
    """
    logger.info("Iniciando sincronização CRM externo", dias=dias)
    
    try:
        data_fim = date.today()
        data_inicio = data_fim - timedelta(days=dias)
        
        conn = get_external_connection()
        
        with conn.cursor() as cursor:
            # Buscar resumo rápido para log
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) as ganhos,
                    SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) as perdidos
                FROM crm_negocio
                WHERE date_create BETWEEN %s AND %s
            """, (data_inicio, data_fim))
            
            resumo = cursor.fetchone()
            
            logger.info(
                "CRM Sync resumo",
                total=resumo['total'],
                ganhos=resumo['ganhos'],
                perdidos=resumo['perdidos']
            )
        
        conn.close()
        
        return {
            "status": "success",
            "periodo": f"{data_inicio} a {data_fim}",
            "total": resumo['total'],
            "ganhos": resumo['ganhos'],
            "perdidos": resumo['perdidos']
        }
        
    except Exception as e:
        logger.error("Erro na sincronização CRM", error=str(e))
        return {"status": "error", "error": str(e)}


@celery_app.task(name="check_crm_connection")
def check_crm_connection():
    """
    Verifica se a conexão com o CRM externo está OK
    Executa a cada minuto
    """
    try:
        conn = get_external_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 as ok")
            result = cursor.fetchone()
        conn.close()
        
        if result and result['ok'] == 1:
            logger.debug("CRM externo OK")
            return {"status": "ok", "connected": True}
        else:
            logger.warning("CRM externo retornou resultado inesperado")
            return {"status": "warning", "connected": False}
            
    except Exception as e:
        logger.error("CRM externo não conectado", error=str(e))
        return {"status": "error", "connected": False, "error": str(e)}


@celery_app.task(name="get_realtime_kpis")
def get_realtime_kpis():
    """
    Obtém KPIs em tempo real do CRM
    Usado para atualizar dashboard
    """
    try:
        conn = get_external_connection()
        
        with conn.cursor() as cursor:
            # KPIs do mês atual
            cursor.execute("""
                SELECT 
                    COUNT(*) AS total_leads,
                    SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
                    SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
                    SUM(CASE WHEN id_state BETWEEN 1 AND 5 THEN 1 ELSE 0 END) AS em_andamento,
                    SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) AS valor_vendido,
                    ROUND(AVG(CASE WHEN id_state = 6 THEN valor ELSE NULL END), 2) AS ticket_medio
                FROM crm_negocio
                WHERE DATE_FORMAT(date_create, '%Y-%m') = DATE_FORMAT(NOW(), '%Y-%m')
            """)
            
            kpis = cursor.fetchone()
            
            # Calcular taxa de conversão
            ganhos = kpis['ganhos'] or 0
            perdidos = kpis['perdidos'] or 0
            total_finalizados = ganhos + perdidos
            taxa_conversao = (ganhos / total_finalizados * 100) if total_finalizados > 0 else 0
            
        conn.close()
        
        return {
            "status": "ok",
            "kpis": {
                "total_leads": kpis['total_leads'] or 0,
                "ganhos": ganhos,
                "perdidos": perdidos,
                "em_andamento": kpis['em_andamento'] or 0,
                "taxa_conversao": round(taxa_conversao, 2),
                "valor_vendido": float(kpis['valor_vendido'] or 0),
                "ticket_medio": float(kpis['ticket_medio'] or 0)
            }
        }
        
    except Exception as e:
        logger.error("Erro ao obter KPIs", error=str(e))
        return {"status": "error", "error": str(e)}

