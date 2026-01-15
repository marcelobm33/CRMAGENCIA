"""
Tasks do Celery
"""
from .sync_google import sync_google_ads, reprocess_last_7_days
from .sync_meta import sync_meta_ads
from .kpi_calculator import calculate_daily_kpis
from .ai_analyst import run_analysis
from .sync_crm import sync_crm_external, check_crm_connection, get_realtime_kpis

__all__ = [
    "sync_google_ads",
    "reprocess_last_7_days",
    "sync_meta_ads",
    "calculate_daily_kpis",
    "run_analysis",
    "sync_crm_external",
    "check_crm_connection",
    "get_realtime_kpis"
]

