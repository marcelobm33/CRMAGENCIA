"""
Serviços da aplicação
"""
from .crm_sync import CRMSyncService
from .external_crm import ExternalCRMClient

__all__ = ["CRMSyncService", "ExternalCRMClient"]

