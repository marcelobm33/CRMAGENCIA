"""
Modelo de atribuição (ligação CRM ↔ Campanhas)
"""
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from database import Base


class AttributionMethod(str, enum.Enum):
    """Métodos de atribuição"""
    UTM = "utm"           # Match por UTM campaign
    GCLID = "gclid"       # Google Click ID
    FBCLID = "fbclid"     # Facebook Click ID
    MANUAL = "manual"     # Atribuição manual pelo usuário
    RULE = "rule"         # Atribuição por regra configurada
    AI = "ai"             # Atribuição sugerida pela IA


class AttributionLink(Base):
    """
    Liga um negócio (deal) a uma campanha
    Permite múltiplas atribuições com diferentes métodos e confiança
    """
    __tablename__ = "attribution_links"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    # Referências
    deal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("crm_deals.id")
    )
    campaign_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ad_campaigns.id")
    )
    
    # Método usado para fazer a atribuição
    method: Mapped[AttributionMethod] = mapped_column(SQLEnum(AttributionMethod))
    
    # Confiança da atribuição (0.0 a 1.0)
    confidence: Mapped[Decimal] = mapped_column(
        Numeric(5, 4),
        default=Decimal("1.0")
    )
    
    # Detalhes do match (para debug/auditoria)
    match_details: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Quem criou (para atribuições manuais)
    created_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
    
    # Relacionamentos
    deal = relationship("CRMDeal", back_populates="attributions")
    campaign = relationship("AdCampaign", back_populates="attributions")
    
    def __repr__(self) -> str:
        return f"<AttributionLink deal={self.deal_id} campaign={self.campaign_id} method={self.method.value}>"

