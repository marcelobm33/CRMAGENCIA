"""
Configurações do Worker
"""
import os
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class WorkerSettings(BaseSettings):
    """Configurações do worker"""
    
    # Banco de dados
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "crm_campanhas"
    postgres_user: str = "admin"
    postgres_password: str = "change_me"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
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
    ai_mode: str = "mock"
    openai_api_key: Optional[str] = None
    
    # Geral
    environment: str = "development"
    log_level: str = "INFO"
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def is_google_configured(self) -> bool:
        return all([
            self.google_ads_developer_token,
            self.google_ads_client_id,
            self.google_ads_client_secret,
            self.google_ads_refresh_token,
            self.google_ads_customer_id
        ])
    
    @property
    def is_meta_configured(self) -> bool:
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
def get_settings() -> WorkerSettings:
    return WorkerSettings()

