"""
Cliente para conectar ao CRM externo (MySQL - netcarrc01)
Leitura apenas (READ-ONLY) - Nenhuma escrita permitida
"""
import os
from typing import Optional, List, Dict, Any
from datetime import datetime, date, timedelta
from decimal import Decimal
import structlog
import pymysql
from pymysql.cursors import DictCursor

logger = structlog.get_logger()


class ExternalCRMClient:
    """
    Cliente para conexão com o CRM externo MySQL (netcarrc01)
    
    IMPORTANTE: Apenas SELECT é permitido!
    Nunca executar INSERT, UPDATE, DELETE, CREATE, ALTER, DROP
    """
    
    def __init__(
        self,
        host: str = None,
        port: int = 3306,
        database: str = None,
        user: str = None,
        password: str = None
    ):
        self.host = host or os.getenv("EXTERNAL_CRM_HOST", "mysql.netcar-rc.com.br")
        self.port = port or int(os.getenv("EXTERNAL_CRM_PORT", "3306"))
        self.database = database or os.getenv("EXTERNAL_CRM_DATABASE", "netcarrc01")
        self.user = user or os.getenv("EXTERNAL_CRM_USER", "")
        self.password = password or os.getenv("EXTERNAL_CRM_PASSWORD", "")
        self._connection = None
    
    def _get_connection(self):
        """Obtém conexão com o banco externo"""
        if self._connection is None or not self._connection.open:
            self._connection = pymysql.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursorclass=DictCursor,
                charset='utf8mb4',
                connect_timeout=10,
                read_timeout=30
            )
        return self._connection
    
    def _execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """
        Executa query READ-ONLY e retorna resultados
        
        SEGURANÇA: Verifica se a query é apenas SELECT
        """
        # Validar que é apenas SELECT
        query_upper = query.strip().upper()
        allowed_commands = ['SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN']
        
        if not any(query_upper.startswith(cmd) for cmd in allowed_commands):
            raise PermissionError("Apenas comandos SELECT são permitidos no CRM externo!")
        
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                return results
        except Exception as e:
            logger.error("Erro ao consultar CRM externo", error=str(e))
            raise
    
    def close(self):
        """Fecha conexão"""
        if self._connection and self._connection.open:
            self._connection.close()
            self._connection = None
    
    # ============================================================
    # MÉTODOS DE CONSULTA AO CRM
    # ============================================================
    
    def get_negocios(
        self,
        data_inicio: date = None,
        data_fim: date = None,
        vendedor_id: int = None,
        origem: str = None,
        estado: int = None,
        limit: int = 1000
    ) -> List[Dict]:
        """
        Busca negócios do CRM com filtros
        
        Estados:
        - 1-5: Em andamento
        - 6: GANHO
        - 7: PERDIDO
        - 8: Arquivado
        """
        query = """
        SELECT 
            n.id_crm_negocio AS id,
            n.titulo AS veiculo,
            n.cliente AS nome_cliente,
            n.celular AS telefone,
            n.email,
            n.origem,
            n.canal,
            n.valor,
            n.id_user AS vendedor_id,
            u.name AS vendedor,
            n.id_state AS estado,
            CASE n.id_state
                WHEN 1 THEN 'novo'
                WHEN 2 THEN 'em_atendimento'
                WHEN 3 THEN 'proposta_enviada'
                WHEN 4 THEN 'em_negociacao'
                WHEN 5 THEN 'fechamento'
                WHEN 6 THEN 'ganho'
                WHEN 7 THEN 'perdido'
                WHEN 8 THEN 'arquivado'
                ELSE 'desconhecido'
            END AS status,
            n.date_create AS data_criacao,
            n.date_update AS data_atualizacao,
            n.motivo_perda,
            n.dias_ultima_negociacao
        FROM crm_negocio n
        LEFT JOIN users u ON n.id_user = u.id_users
        WHERE 1=1
        """
        params = []
        
        if data_inicio:
            query += " AND n.date_create >= %s"
            params.append(data_inicio)
        
        if data_fim:
            query += " AND n.date_create <= %s"
            params.append(data_fim)
        
        if vendedor_id:
            query += " AND n.id_user = %s"
            params.append(vendedor_id)
        
        if origem:
            query += " AND n.origem = %s"
            params.append(origem)
        
        if estado:
            query += " AND n.id_state = %s"
            params.append(estado)
        
        query += f" ORDER BY n.date_create DESC LIMIT {limit}"
        
        return self._execute_query(query, tuple(params))
    
    def get_negocios_ganhos(self, data_inicio: date = None, data_fim: date = None) -> List[Dict]:
        """Busca apenas negócios GANHOS (estado = 6)"""
        return self.get_negocios(data_inicio=data_inicio, data_fim=data_fim, estado=6)
    
    def get_negocios_perdidos(self, data_inicio: date = None, data_fim: date = None) -> List[Dict]:
        """Busca apenas negócios PERDIDOS (estado = 7)"""
        return self.get_negocios(data_inicio=data_inicio, data_fim=data_fim, estado=7)
    
    def get_vendedores(self) -> List[Dict]:
        """Lista vendedores ativos"""
        query = """
        SELECT 
            id_users AS id,
            name AS nome,
            email,
            id_profile AS perfil,
            CASE id_profile
                WHEN 1 THEN 'admin'
                WHEN 2 THEN 'gerente'
                WHEN 3 THEN 'vendedor'
                ELSE 'outro'
            END AS tipo_perfil,
            status
        FROM users
        WHERE status = 'S'
        ORDER BY name
        """
        return self._execute_query(query)
    
    def get_origens_disponiveis(self) -> List[str]:
        """Lista todas as origens únicas"""
        query = """
        SELECT DISTINCT origem
        FROM crm_negocio
        WHERE origem IS NOT NULL AND origem != ''
        ORDER BY origem
        """
        results = self._execute_query(query)
        return [r['origem'] for r in results]
    
    def get_resumo_mensal(self, ano: int = None, mes: int = None) -> Dict:
        """Resumo de KPIs do mês"""
        if not ano:
            ano = datetime.now().year
        if not mes:
            mes = datetime.now().month
        
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
        results = self._execute_query(query, (ano, mes))
        
        if results:
            r = results[0]
            ganhos = r['ganhos'] or 0
            perdidos = r['perdidos'] or 0
            total_finalizados = ganhos + perdidos
            taxa_conversao = (ganhos / total_finalizados * 100) if total_finalizados > 0 else 0
            
            return {
                'periodo': f"{ano}-{mes:02d}",
                'total_leads': r['total_leads'] or 0,
                'ganhos': ganhos,
                'perdidos': perdidos,
                'em_andamento': r['em_andamento'] or 0,
                'taxa_conversao': round(taxa_conversao, 2),
                'valor_vendido': float(r['valor_vendido'] or 0),
                'ticket_medio': float(r['ticket_medio'] or 0)
            }
        return {}
    
    def get_resumo_por_vendedor(self, data_inicio: date = None, data_fim: date = None) -> List[Dict]:
        """Resumo de performance por vendedor"""
        if not data_inicio:
            data_inicio = date.today().replace(day=1)
        if not data_fim:
            data_fim = date.today()
        
        query = """
        SELECT 
            n.id_user AS vendedor_id,
            u.name AS vendedor,
            COUNT(*) AS total_leads,
            SUM(CASE WHEN n.id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN n.id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
            SUM(CASE WHEN n.id_state BETWEEN 1 AND 5 THEN 1 ELSE 0 END) AS em_andamento,
            SUM(CASE WHEN n.id_state = 6 THEN n.valor ELSE 0 END) AS valor_vendido,
            ROUND(AVG(CASE WHEN n.id_state = 6 THEN n.valor ELSE NULL END), 2) AS ticket_medio
        FROM crm_negocio n
        LEFT JOIN users u ON n.id_user = u.id_users
        WHERE n.date_create BETWEEN %s AND %s
        GROUP BY n.id_user, u.name
        ORDER BY valor_vendido DESC
        """
        results = self._execute_query(query, (data_inicio, data_fim))
        
        for r in results:
            ganhos = r['ganhos'] or 0
            perdidos = r['perdidos'] or 0
            total = ganhos + perdidos
            r['taxa_conversao'] = round((ganhos / total * 100) if total > 0 else 0, 2)
        
        return results
    
    def get_resumo_por_origem(self, data_inicio: date = None, data_fim: date = None) -> List[Dict]:
        """Resumo de performance por origem (agrupada)"""
        if not data_inicio:
            data_inicio = date.today().replace(day=1)
        if not data_fim:
            data_fim = date.today()
        
        query = """
        SELECT 
            CASE 
                WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
                WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
                WHEN origem IN ('SITE') THEN 'SITE'
                WHEN origem IN ('WEBMOTORS', 'ICARROS', 'MEUCARRONOVO', 'MERCADO LIVRE', 'MOBIAUTO', 'AUTOLINE', 'POACARROS', 'SOCARRAO', 'Autocarro') THEN 'PORTAIS'
                WHEN origem IN ('SHOWROOM', 'NA PISTA', 'FEIRÃO') THEN 'PRESENCIAL'
                WHEN origem IN ('WHATSAPP', 'TELEFONE', 'TELEMARKETING') THEN 'DIRETO'
                WHEN origem IN ('INDICACAO', 'INDICAÇÃO CAMPANHA', 'REDE RELACIONAMENTO') THEN 'INDICACAO'
                ELSE 'OUTROS'
            END AS grupo_origem,
            COUNT(*) AS total_leads,
            SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
            SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) AS valor_vendido,
            ROUND(AVG(CASE WHEN id_state = 6 THEN valor ELSE NULL END), 2) AS ticket_medio
        FROM crm_negocio
        WHERE date_create BETWEEN %s AND %s
        GROUP BY grupo_origem
        ORDER BY ganhos DESC
        """
        results = self._execute_query(query, (data_inicio, data_fim))
        
        for r in results:
            ganhos = r['ganhos'] or 0
            perdidos = r['perdidos'] or 0
            total = ganhos + perdidos
            r['taxa_conversao'] = round((ganhos / total * 100) if total > 0 else 0, 2)
        
        return results
    
    def get_motivos_perda(self, data_inicio: date = None, data_fim: date = None, limit: int = 20) -> List[Dict]:
        """Top motivos de perda"""
        if not data_inicio:
            data_inicio = date.today().replace(day=1)
        if not data_fim:
            data_fim = date.today()
        
        query = """
        SELECT 
            motivo_perda,
            COUNT(*) AS quantidade,
            ROUND(COUNT(*) * 100.0 / (
                SELECT COUNT(*) FROM crm_negocio 
                WHERE id_state = 7 
                AND date_create BETWEEN %s AND %s
            ), 2) AS percentual
        FROM crm_negocio
        WHERE id_state = 7
          AND motivo_perda IS NOT NULL
          AND motivo_perda != ''
          AND date_create BETWEEN %s AND %s
        GROUP BY motivo_perda
        ORDER BY quantidade DESC
        LIMIT %s
        """
        return self._execute_query(query, (data_inicio, data_fim, data_inicio, data_fim, limit))
    
    def get_funil(self) -> List[Dict]:
        """Estado atual do funil (leads ativos)"""
        query = """
        SELECT 
            id_state,
            CASE id_state
                WHEN 1 THEN '1. Novo'
                WHEN 2 THEN '2. Em Atendimento'
                WHEN 3 THEN '3. Proposta Enviada'
                WHEN 4 THEN '4. Em Negociação'
                WHEN 5 THEN '5. Fechamento'
                WHEN 6 THEN '6. GANHO'
                WHEN 7 THEN '7. PERDIDO'
                WHEN 8 THEN '8. Arquivado'
            END AS etapa,
            COUNT(*) AS quantidade,
            SUM(valor) AS valor_total,
            ROUND(AVG(valor), 2) AS ticket_medio
        FROM crm_negocio
        GROUP BY id_state
        ORDER BY id_state
        """
        return self._execute_query(query)
    
    def get_leads_parados(self, dias: int = 7) -> List[Dict]:
        """Leads parados há mais de X dias (apenas ativos)"""
        query = """
        SELECT 
            n.id_crm_negocio AS id,
            n.titulo AS veiculo,
            n.cliente AS nome_cliente,
            n.origem,
            u.name AS vendedor,
            n.id_state AS estado,
            n.valor,
            n.date_create AS data_criacao,
            n.date_update AS ultima_atualizacao,
            DATEDIFF(NOW(), n.date_update) AS dias_parado
        FROM crm_negocio n
        LEFT JOIN users u ON n.id_user = u.id_users
        WHERE n.id_state BETWEEN 1 AND 5
          AND DATEDIFF(NOW(), n.date_update) > %s
        ORDER BY dias_parado DESC
        LIMIT 100
        """
        return self._execute_query(query, (dias,))
    
    def get_comparativo_meta_google(self, data_inicio: date = None, data_fim: date = None) -> Dict:
        """Comparativo direto META vs GOOGLE"""
        if not data_inicio:
            data_inicio = date.today().replace(day=1)
        if not data_fim:
            data_fim = date.today()
        
        query = """
        SELECT 
            CASE 
                WHEN origem IN ('FACEBOOK', 'INSTAGRAM') THEN 'META'
                WHEN origem IN ('Google', 'GOOGLE') THEN 'GOOGLE'
            END AS plataforma,
            COUNT(*) AS total_leads,
            SUM(CASE WHEN id_state = 6 THEN 1 ELSE 0 END) AS ganhos,
            SUM(CASE WHEN id_state = 7 THEN 1 ELSE 0 END) AS perdidos,
            SUM(CASE WHEN id_state = 6 THEN valor ELSE 0 END) AS valor_vendido,
            ROUND(AVG(CASE WHEN id_state = 6 THEN valor ELSE NULL END), 2) AS ticket_medio
        FROM crm_negocio
        WHERE origem IN ('FACEBOOK', 'INSTAGRAM', 'Google', 'GOOGLE')
          AND date_create BETWEEN %s AND %s
        GROUP BY plataforma
        """
        results = self._execute_query(query, (data_inicio, data_fim))
        
        comparativo = {'META': None, 'GOOGLE': None}
        for r in results:
            if r['plataforma']:
                ganhos = r['ganhos'] or 0
                perdidos = r['perdidos'] or 0
                total = ganhos + perdidos
                r['taxa_conversao'] = round((ganhos / total * 100) if total > 0 else 0, 2)
                comparativo[r['plataforma']] = r
        
        return comparativo
    
    def test_connection(self) -> bool:
        """Testa a conexão com o banco"""
        try:
            query = "SELECT 1 as ok"
            result = self._execute_query(query)
            return result and result[0].get('ok') == 1
        except Exception as e:
            logger.error("Falha ao testar conexão com CRM externo", error=str(e))
            return False


# Singleton para uso global
_external_crm_client = None

def get_external_crm() -> ExternalCRMClient:
    """Retorna instância singleton do cliente CRM"""
    global _external_crm_client
    if _external_crm_client is None:
        _external_crm_client = ExternalCRMClient()
    return _external_crm_client

