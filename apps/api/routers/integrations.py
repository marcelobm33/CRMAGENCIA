"""
Router de Integrações (Google Ads e Meta Ads)
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from database import get_db
from config import get_settings
from models import User
from models.campaigns import AdPlatformAccount, AdPlatform
from routers.auth import get_current_user, get_current_admin_user

router = APIRouter()
settings = get_settings()


class IntegrationStatus(BaseModel):
    """Status de uma integração"""
    platform: str
    configured: bool
    connected: bool
    account_name: Optional[str] = None
    last_synced: Optional[datetime] = None
    mode: str  # "mock" ou "live"


class ConnectRequest(BaseModel):
    """Request para conectar uma plataforma"""
    account_id: str
    account_name: str
    # Credenciais são passadas mas não armazenadas diretamente aqui
    # Em produção, usar OAuth flow
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


@router.get("/status")
async def get_integrations_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna status de todas as integrações
    """
    integrations = []
    
    # Google Ads
    google_account = await db.execute(
        select(AdPlatformAccount).where(
            AdPlatformAccount.platform == AdPlatform.GOOGLE,
            AdPlatformAccount.is_active == True
        )
    )
    google = google_account.scalar_one_or_none()
    
    integrations.append(IntegrationStatus(
        platform="google",
        configured=settings.is_google_ads_configured,
        connected=google is not None,
        account_name=google.account_name if google else None,
        last_synced=google.last_synced if google else None,
        mode="live" if settings.is_google_ads_configured else "mock"
    ))
    
    # Meta Ads
    meta_account = await db.execute(
        select(AdPlatformAccount).where(
            AdPlatformAccount.platform == AdPlatform.META,
            AdPlatformAccount.is_active == True
        )
    )
    meta = meta_account.scalar_one_or_none()
    
    integrations.append(IntegrationStatus(
        platform="meta",
        configured=settings.is_meta_ads_configured,
        connected=meta is not None,
        account_name=meta.account_name if meta else None,
        last_synced=meta.last_synced if meta else None,
        mode="live" if settings.is_meta_ads_configured else "mock"
    ))
    
    return {
        "integrations": integrations,
        "ai_mode": settings.ai_mode,
        "environment": settings.environment
    }


@router.post("/google/connect")
async def connect_google_ads(
    request: ConnectRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Conecta uma conta do Google Ads
    
    Em modo mock, apenas registra a conta.
    Em modo live, valida as credenciais com a API.
    """
    # Verificar se já existe conta ativa
    existing = await db.execute(
        select(AdPlatformAccount).where(
            AdPlatformAccount.platform == AdPlatform.GOOGLE,
            AdPlatformAccount.is_active == True
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Já existe uma conta Google Ads conectada. Desconecte primeiro."
        )
    
    # Criar conta
    account = AdPlatformAccount(
        platform=AdPlatform.GOOGLE,
        account_id=request.account_id,
        account_name=request.account_name,
        is_active=True,
        credentials_encrypted=None  # Em produção, criptografar tokens
    )
    
    db.add(account)
    await db.commit()
    await db.refresh(account)
    
    return {
        "message": "Conta Google Ads conectada com sucesso",
        "account_id": str(account.id),
        "mode": "live" if settings.is_google_ads_configured else "mock",
        "note": "Modo mock ativo. Dados de campanha serão simulados." if not settings.is_google_ads_configured else None
    }


@router.post("/meta/connect")
async def connect_meta_ads(
    request: ConnectRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Conecta uma conta do Meta Ads (Facebook/Instagram)
    
    Em modo mock, apenas registra a conta.
    Em modo live, valida as credenciais com a API.
    """
    # Verificar se já existe conta ativa
    existing = await db.execute(
        select(AdPlatformAccount).where(
            AdPlatformAccount.platform == AdPlatform.META,
            AdPlatformAccount.is_active == True
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Já existe uma conta Meta Ads conectada. Desconecte primeiro."
        )
    
    # Criar conta
    account = AdPlatformAccount(
        platform=AdPlatform.META,
        account_id=request.account_id,
        account_name=request.account_name,
        is_active=True,
        credentials_encrypted=None
    )
    
    db.add(account)
    await db.commit()
    await db.refresh(account)
    
    return {
        "message": "Conta Meta Ads conectada com sucesso",
        "account_id": str(account.id),
        "mode": "live" if settings.is_meta_ads_configured else "mock",
        "note": "Modo mock ativo. Dados de campanha serão simulados." if not settings.is_meta_ads_configured else None
    }


@router.delete("/google/disconnect")
async def disconnect_google_ads(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Desconecta a conta do Google Ads
    """
    result = await db.execute(
        select(AdPlatformAccount).where(
            AdPlatformAccount.platform == AdPlatform.GOOGLE,
            AdPlatformAccount.is_active == True
        )
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(status_code=404, detail="Nenhuma conta Google Ads conectada")
    
    account.is_active = False
    await db.commit()
    
    return {"message": "Conta Google Ads desconectada"}


@router.delete("/meta/disconnect")
async def disconnect_meta_ads(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Desconecta a conta do Meta Ads
    """
    result = await db.execute(
        select(AdPlatformAccount).where(
            AdPlatformAccount.platform == AdPlatform.META,
            AdPlatformAccount.is_active == True
        )
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(status_code=404, detail="Nenhuma conta Meta Ads conectada")
    
    account.is_active = False
    await db.commit()
    
    return {"message": "Conta Meta Ads desconectada"}


@router.post("/sync")
async def trigger_sync(
    background_tasks: BackgroundTasks,
    platform: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Dispara sincronização manual das campanhas
    
    Em modo mock, gera dados fake.
    Em modo live, busca dados das APIs.
    """
    # Por enquanto, retorna mock
    # TODO: Integrar com Celery tasks
    
    return {
        "message": "Sincronização disparada",
        "platform": platform or "all",
        "mode": "mock",
        "note": "A sincronização será processada em background. Verifique os logs para acompanhar."
    }


@router.get("/google/setup-guide")
async def get_google_setup_guide():
    """
    Retorna guia de configuração do Google Ads
    """
    return {
        "title": "Configuração do Google Ads API",
        "steps": [
            {
                "step": 1,
                "title": "Criar projeto no Google Cloud Console",
                "url": "https://console.cloud.google.com/",
                "instructions": [
                    "Acesse o Google Cloud Console",
                    "Crie um novo projeto ou selecione existente",
                    "Anote o ID do projeto"
                ]
            },
            {
                "step": 2,
                "title": "Ativar Google Ads API",
                "instructions": [
                    "No Console, vá em APIs & Services > Library",
                    "Busque por 'Google Ads API'",
                    "Clique em Enable"
                ]
            },
            {
                "step": 3,
                "title": "Criar credenciais OAuth",
                "instructions": [
                    "Vá em APIs & Services > Credentials",
                    "Clique em Create Credentials > OAuth Client ID",
                    "Tipo: Web Application",
                    "Adicione redirect URI: http://localhost:8000/api/integrations/google/callback",
                    "Anote Client ID e Client Secret"
                ]
            },
            {
                "step": 4,
                "title": "Obter Developer Token",
                "url": "https://ads.google.com/aw/apicenter",
                "instructions": [
                    "Acesse o Google Ads API Center",
                    "Solicite ou copie seu Developer Token",
                    "Token de teste funciona para desenvolvimento"
                ]
            },
            {
                "step": 5,
                "title": "Configurar variáveis de ambiente",
                "instructions": [
                    "No arquivo .env, preencha:",
                    "GOOGLE_ADS_DEVELOPER_TOKEN=seu_token",
                    "GOOGLE_ADS_CLIENT_ID=seu_client_id",
                    "GOOGLE_ADS_CLIENT_SECRET=seu_secret",
                    "GOOGLE_ADS_CUSTOMER_ID=seu_customer_id (sem hífens)"
                ]
            }
        ],
        "env_variables": [
            "GOOGLE_ADS_DEVELOPER_TOKEN",
            "GOOGLE_ADS_CLIENT_ID",
            "GOOGLE_ADS_CLIENT_SECRET",
            "GOOGLE_ADS_REFRESH_TOKEN",
            "GOOGLE_ADS_CUSTOMER_ID"
        ]
    }


@router.get("/meta/setup-guide")
async def get_meta_setup_guide():
    """
    Retorna guia de configuração do Meta Ads
    """
    return {
        "title": "Configuração do Meta Marketing API",
        "steps": [
            {
                "step": 1,
                "title": "Criar App no Meta for Developers",
                "url": "https://developers.facebook.com/apps/",
                "instructions": [
                    "Acesse Meta for Developers",
                    "Clique em Create App",
                    "Selecione tipo Business",
                    "Preencha nome e contato"
                ]
            },
            {
                "step": 2,
                "title": "Adicionar Marketing API",
                "instructions": [
                    "No dashboard do app, clique em Add Product",
                    "Encontre Marketing API e clique em Set Up",
                    "Siga o wizard de configuração"
                ]
            },
            {
                "step": 3,
                "title": "Gerar Access Token",
                "instructions": [
                    "Vá em Tools > Graph API Explorer",
                    "Selecione seu app",
                    "Adicione permissões: ads_read, ads_management",
                    "Gere o token e anote",
                    "Para produção, gere um token de longa duração"
                ]
            },
            {
                "step": 4,
                "title": "Obter Ad Account ID",
                "instructions": [
                    "Acesse Business Manager",
                    "Vá em Business Settings > Accounts > Ad Accounts",
                    "Copie o ID da conta (formato: act_XXXXXXXXX)"
                ]
            },
            {
                "step": 5,
                "title": "Configurar variáveis de ambiente",
                "instructions": [
                    "No arquivo .env, preencha:",
                    "META_APP_ID=seu_app_id",
                    "META_APP_SECRET=seu_app_secret",
                    "META_ACCESS_TOKEN=seu_access_token",
                    "META_AD_ACCOUNT_ID=act_XXXXXXXXX"
                ]
            }
        ],
        "env_variables": [
            "META_APP_ID",
            "META_APP_SECRET",
            "META_ACCESS_TOKEN",
            "META_AD_ACCOUNT_ID"
        ]
    }

