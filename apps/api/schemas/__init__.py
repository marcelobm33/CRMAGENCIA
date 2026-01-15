"""
Schemas Pydantic para validação e serialização
"""
from .crm import (
    CRMDealCreate,
    CRMDealUpdate,
    CRMDealResponse,
    CRMDealListResponse,
    CRMImportResult
)
from .campaigns import (
    AdCampaignResponse,
    AdSpendDailyResponse,
    AdPlatformAccountResponse
)
from .analytics import (
    KPISnapshotResponse,
    DashboardOverview,
    ChannelMetrics,
    VendedorMetrics,
    FunnelMetrics
)
from .ai import (
    AIRecommendationResponse,
    AIRecommendationUpdate
)
from .auth import (
    UserCreate,
    UserResponse,
    Token,
    TokenData,
    LoginRequest
)

__all__ = [
    # CRM
    "CRMDealCreate",
    "CRMDealUpdate", 
    "CRMDealResponse",
    "CRMDealListResponse",
    "CRMImportResult",
    # Campaigns
    "AdCampaignResponse",
    "AdSpendDailyResponse",
    "AdPlatformAccountResponse",
    # Analytics
    "KPISnapshotResponse",
    "DashboardOverview",
    "ChannelMetrics",
    "VendedorMetrics",
    "FunnelMetrics",
    # AI
    "AIRecommendationResponse",
    "AIRecommendationUpdate",
    # Auth
    "UserCreate",
    "UserResponse",
    "Token",
    "TokenData",
    "LoginRequest"
]

