"""
Serviço de sincronização do CRM externo para o banco local
"""
import structlog
from datetime import datetime, date, timedelta
from typing import Optional, List
from decimal import Decimal
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from .external_crm import ExternalCRMClient, get_external_crm
from models.crm import CRMDeal, DealStatus

logger = structlog.get_logger()


class CRMSyncService:
    """
    Sincroniza dados do CRM externo (MySQL) para o banco local (PostgreSQL)
    """
    
    def __init__(self, db: AsyncSession, external_client: ExternalCRMClient = None):
        self.db = db
        self.external = external_client or get_external_crm()
    
    def _map_status(self, estado: int) -> DealStatus:
        """Mapeia estado do CRM externo para DealStatus"""
        if estado == 6:
            return DealStatus.GANHO
        elif estado == 7:
            return DealStatus.PERDIDO
        else:
            return DealStatus.ABERTO
    
    def _map_canal(self, origem: str) -> str:
        """Mapeia origem para canal padronizado"""
        if not origem:
            return None
        
        origem_upper = origem.upper()
        
        if origem_upper in ['FACEBOOK', 'INSTAGRAM']:
            return 'Meta'
        elif origem_upper == 'GOOGLE':
            return 'Google'
        elif origem_upper == 'SITE':
            return 'Site'
        elif origem_upper in ['WEBMOTORS', 'ICARROS', 'MEUCARRONOVO', 'MERCADO LIVRE', 'MOBIAUTO', 'AUTOLINE', 'POACARROS', 'SOCARRAO', 'AUTOCARRO']:
            return 'Portais'
        elif origem_upper in ['SHOWROOM', 'NA PISTA', 'FEIRÃO']:
            return 'Presencial'
        elif origem_upper in ['WHATSAPP', 'TELEFONE', 'TELEMARKETING']:
            return 'Direto'
        elif origem_upper in ['INDICACAO', 'INDICAÇÃO CAMPANHA', 'REDE RELACIONAMENTO']:
            return 'Indicação'
        else:
            return origem
    
    def _map_utm_source(self, origem: str) -> Optional[str]:
        """Mapeia origem para utm_source"""
        if not origem:
            return None
        
        origem_upper = origem.upper()
        
        if origem_upper == 'FACEBOOK':
            return 'facebook'
        elif origem_upper == 'INSTAGRAM':
            return 'instagram'
        elif origem_upper == 'GOOGLE':
            return 'google'
        else:
            return origem.lower()
    
    async def sync_negocios(
        self,
        data_inicio: date = None,
        data_fim: date = None,
        full_sync: bool = False
    ) -> dict:
        """
        Sincroniza negócios do CRM externo
        
        Args:
            data_inicio: Data inicial para sincronização
            data_fim: Data final para sincronização
            full_sync: Se True, resincroniza tudo (não apenas novos)
        
        Returns:
            Estatísticas da sincronização
        """
        if not data_inicio:
            # Por padrão, sincroniza últimos 7 dias
            data_inicio = date.today() - timedelta(days=7)
        if not data_fim:
            data_fim = date.today()
        
        logger.info("Iniciando sincronização CRM", 
            data_inicio=str(data_inicio), 
            data_fim=str(data_fim),
            full_sync=full_sync
        )
        
        stats = {
            'total': 0,
            'novos': 0,
            'atualizados': 0,
            'erros': 0
        }
        
        try:
            # Buscar negócios do CRM externo
            negocios = self.external.get_negocios(
                data_inicio=data_inicio,
                data_fim=data_fim,
                limit=10000  # Limite alto para sync
            )
            
            stats['total'] = len(negocios)
            logger.info(f"Encontrados {len(negocios)} negócios para sincronizar")
            
            for negocio in negocios:
                try:
                    # Verificar se já existe (pelo id externo)
                    external_id = str(negocio['id'])
                    
                    # Buscar deal existente
                    # Usamos observacoes para guardar o ID externo temporariamente
                    # Em produção, adicionar coluna external_id na tabela
                    result = await self.db.execute(
                        select(CRMDeal).where(
                            CRMDeal.observacoes.contains(f"[EXT_ID:{external_id}]")
                        )
                    )
                    existing = result.scalar_one_or_none()
                    
                    if existing and not full_sync:
                        # Atualizar apenas se mudou de status
                        new_status = self._map_status(negocio['estado'])
                        if existing.status != new_status:
                            existing.status = new_status
                            existing.motivo_perda = negocio.get('motivo_perda')
                            if new_status != DealStatus.ABERTO:
                                existing.data_fechamento = negocio.get('data_atualizacao')
                            stats['atualizados'] += 1
                    else:
                        # Criar novo deal
                        deal = CRMDeal(
                            data_criacao=negocio.get('data_criacao') or datetime.now(),
                            data_fechamento=negocio.get('data_atualizacao') if negocio['estado'] in [6, 7] else None,
                            status=self._map_status(negocio['estado']),
                            motivo_perda=negocio.get('motivo_perda'),
                            valor=Decimal(str(negocio.get('valor') or 0)),
                            lucro_bruto=Decimal("0"),  # CRM externo não tem essa info
                            vendedor=negocio.get('vendedor') or 'Não Atribuído',
                            telefone=negocio.get('telefone'),
                            email=negocio.get('email'),
                            nome_cliente=negocio.get('nome_cliente'),
                            origem=negocio.get('origem'),
                            canal=self._map_canal(negocio.get('origem')),
                            utm_source=self._map_utm_source(negocio.get('origem')),
                            veiculo_interesse=negocio.get('veiculo'),
                            observacoes=f"[EXT_ID:{external_id}] Sincronizado do CRM em {datetime.now().isoformat()}"
                        )
                        self.db.add(deal)
                        stats['novos'] += 1
                
                except Exception as e:
                    logger.error("Erro ao sincronizar negócio", 
                        negocio_id=negocio.get('id'), 
                        error=str(e)
                    )
                    stats['erros'] += 1
            
            await self.db.commit()
            
            logger.info("Sincronização CRM concluída", **stats)
            return stats
            
        except Exception as e:
            logger.error("Erro na sincronização CRM", error=str(e))
            raise
    
    async def get_last_sync_time(self) -> Optional[datetime]:
        """Retorna data/hora da última sincronização"""
        result = await self.db.execute(
            select(func.max(CRMDeal.created_at))
            .where(CRMDeal.observacoes.contains("[EXT_ID:"))
        )
        return result.scalar()
    
    async def get_sync_stats(self) -> dict:
        """Estatísticas de sincronização"""
        # Total sincronizado
        result = await self.db.execute(
            select(func.count(CRMDeal.id))
            .where(CRMDeal.observacoes.contains("[EXT_ID:"))
        )
        total_sincronizado = result.scalar() or 0
        
        # Total no CRM externo (últimos 30 dias)
        try:
            resumo = self.external.get_resumo_mensal()
            total_externo = resumo.get('total_leads', 0)
        except:
            total_externo = 'N/A'
        
        last_sync = await self.get_last_sync_time()
        
        return {
            'total_sincronizado': total_sincronizado,
            'total_crm_externo': total_externo,
            'ultima_sincronizacao': last_sync.isoformat() if last_sync else None,
            'conexao_ok': self.external.test_connection()
        }

