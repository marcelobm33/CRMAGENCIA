"""
Configurações da aplicação usando Pydantic Settings
"""
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações carregadas de variáveis de ambiente"""
    
    # Banco de dados
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "crm_campanhas"
    postgres_user: str = "admin"
    postgres_password: str = "change_me"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # API
    api_secret_key: str = "dev_secret_key_change_in_prod"
    api_admin_email: str = "admin@revenda.com"
    api_admin_password: str = "admin123"
    
    # Google Ads
    google_ads_developer_token: Optional[str] = None
    google_ads_client_id: Optional[str] = None
    google_ads_client_secret: Optional[str] = None
    google_ads_refresh_token: Optional[str] = None
    google_ads_customer_id: Optional[str] = None
    
    # Meta Ads
    meta_app_id: Optional[str] = None
    meta_app_secret: Optional[str] = None
    meta_access_token: Optional[str] = None
    meta_ad_account_id: Optional[str] = None
    
    # IA
    ai_mode: str = "mock"  # mock ou openai
    openai_api_key: Optional[str] = None
    
    # Geral
    environment: str = "development"
    log_level: str = "INFO"
    
    @property
    def database_url(self) -> str:
        """URL de conexão do banco de dados (async)"""
        # Usar SQLite por enquanto (mais simples)
        return "sqlite+aiosqlite:///./crm_ia.db"
    
    @property
    def database_url_sync(self) -> str:
        """URL de conexão do banco de dados (sync - para Alembic)"""
        return "sqlite:///./crm_ia.db"
    
    @property
    def is_google_ads_configured(self) -> bool:
        """Verifica se Google Ads está configurado"""
        return all([
            self.google_ads_developer_token,
            self.google_ads_client_id,
            self.google_ads_client_secret,
            self.google_ads_refresh_token,
            self.google_ads_customer_id
        ])
    
    @property
    def is_meta_ads_configured(self) -> bool:
        """Verifica se Meta Ads está configurado"""
        return all([
            self.meta_app_id,
            self.meta_app_secret,
            self.meta_access_token,
            self.meta_ad_account_id
        ])
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Retorna instância cacheada das configurações"""
    return Settings()

