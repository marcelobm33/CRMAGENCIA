"""
Modelos SQLAlchemy do sistema
"""
from .crm import CRMDeal
from .campaigns import Campaign, CampaignInsight
from .attribution import AttributionLink
from .analytics import KPISnapshot
from .ai import AIRecommendation
from .users import User

__all__ = [
    "CRMDeal",
    "Campaign",
    "CampaignInsight",
    "AttributionLink",
    "KPISnapshot",
    "AIRecommendation",
    "User"
]

