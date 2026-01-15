"""
Router para sincronização com CRM externo
"""
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import User
from services.external_crm import get_external_crm
from services.crm_sync import CRMSyncService
from routers.auth import get_current_user, get_current_admin_user

router = APIRouter()


@router.get("/status")
async def get_crm_sync_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Status da conexão e sincronização com CRM externo
    """
    sync_service = CRMSyncService(db)
    stats = await sync_service.get_sync_stats()
    
    return {
        "crm_externo": {
            "host": "mysql.netcar-rc.com.br",
            "database": "netcarrc01",
            "conexao": stats['conexao_ok']
        },
        "sincronizacao": {
            "total_sincronizado": stats['total_sincronizado'],
            "total_crm_externo": stats['total_crm_externo'],
            "ultima_sincronizacao": stats['ultima_sincronizacao']
        }
    }


@router.post("/sync")
async def trigger_sync(
    background_tasks: BackgroundTasks,
    dias: int = Query(7, ge=1, le=365),
    full_sync: bool = False,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Dispara sincronização do CRM externo
    
    Args:
        dias: Quantidade de dias para sincronizar (padrão: 7)
        full_sync: Se True, resincroniza tudo (padrão: False)
    """
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias)
    
    sync_service = CRMSyncService(db)
    
    # Executar sincronização
    stats = await sync_service.sync_negocios(
        data_inicio=data_inicio,
        data_fim=data_fim,
        full_sync=full_sync
    )
    
    return {
        "message": "Sincronização concluída",
        "periodo": {
            "inicio": data_inicio.isoformat(),
            "fim": data_fim.isoformat()
        },
        "estatisticas": stats
    }


@router.get("/preview")
async def preview_external_crm(
    dias: int = Query(7, ge=1, le=30),
    current_user: User = Depends(get_current_user)
):
    """
    Preview dos dados do CRM externo (sem sincronizar)
    """
    external = get_external_crm()
    
    if not external.test_connection():
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar ao CRM externo"
        )
    
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias)
    
    # Buscar resumo
    resumo = external.get_resumo_mensal()
    por_vendedor = external.get_resumo_por_vendedor(data_inicio, data_fim)
    por_origem = external.get_resumo_por_origem(data_inicio, data_fim)
    motivos = external.get_motivos_perda(data_inicio, data_fim, limit=10)
    
    return {
        "periodo": {
            "inicio": data_inicio.isoformat(),
            "fim": data_fim.isoformat()
        },
        "resumo_mes": resumo,
        "por_vendedor": por_vendedor[:5],  # Top 5
        "por_origem": por_origem,
        "motivos_perda": motivos[:5]  # Top 5
    }


@router.get("/realtime/resumo")
async def get_realtime_resumo(
    current_user: User = Depends(get_current_user)
):
    """
    Dados em tempo real do CRM externo - Resumo do mês
    """
    external = get_external_crm()
    
    try:
        resumo = external.get_resumo_mensal()
        return resumo
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro ao consultar CRM: {str(e)}")


@router.get("/realtime/vendedores")
async def get_realtime_vendedores(
    dias: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user)
):
    """
    Performance por vendedor em tempo real
    """
    external = get_external_crm()
    
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias)
    
    try:
        return external.get_resumo_por_vendedor(data_inicio, data_fim)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro ao consultar CRM: {str(e)}")


@router.get("/realtime/origens")
async def get_realtime_origens(
    dias: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user)
):
    """
    Performance por origem em tempo real
    """
    external = get_external_crm()
    
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias)
    
    try:
        return external.get_resumo_por_origem(data_inicio, data_fim)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro ao consultar CRM: {str(e)}")


@router.get("/realtime/funil")
async def get_realtime_funil(
    current_user: User = Depends(get_current_user)
):
    """
    Estado atual do funil em tempo real
    """
    external = get_external_crm()
    
    try:
        return external.get_funil()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro ao consultar CRM: {str(e)}")


@router.get("/realtime/motivos-perda")
async def get_realtime_motivos_perda(
    dias: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user)
):
    """
    Motivos de perda em tempo real
    """
    external = get_external_crm()
    
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias)
    
    try:
        return external.get_motivos_perda(data_inicio, data_fim)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro ao consultar CRM: {str(e)}")


@router.get("/realtime/leads-parados")
async def get_realtime_leads_parados(
    dias: int = Query(7, ge=1, le=30),
    current_user: User = Depends(get_current_user)
):
    """
    Leads parados há mais de X dias
    """
    external = get_external_crm()
    
    try:
        return external.get_leads_parados(dias)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro ao consultar CRM: {str(e)}")


@router.get("/realtime/meta-vs-google")
async def get_realtime_meta_vs_google(
    dias: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user)
):
    """
    Comparativo META vs GOOGLE em tempo real
    """
    external = get_external_crm()
    
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias)
    
    try:
        return external.get_comparativo_meta_google(data_inicio, data_fim)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro ao consultar CRM: {str(e)}")

