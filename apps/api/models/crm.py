"""
Modelo de negócios do CRM (Deals)
"""
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Text, Numeric, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from database import Base


class DealStatus(str, enum.Enum):
    """Status possíveis de um negócio"""
    ABERTO = "aberto"
    GANHO = "ganho"
    PERDIDO = "perdido"


class CRMDeal(Base):
    """
    Representa um negócio/lead do CRM
    Contém informações do cliente, vendedor, valores e rastreamento UTM
    """
    __tablename__ = "crm_deals"
    
    # Identificador
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    # Datas
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
    data_fechamento: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Status e resultado
    status: Mapped[DealStatus] = mapped_column(
        SQLEnum(DealStatus),
        default=DealStatus.ABERTO
    )
    motivo_perda: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )
    
    # Valores
    valor: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        default=Decimal("0")
    )
    lucro_bruto: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        default=Decimal("0")
    )
    
    # Vendedor
    vendedor: Mapped[str] = mapped_column(String(255))
    
    # Contato do cliente
    telefone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    nome_cliente: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Origem e tracking
    origem: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    canal: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # UTM Parameters
    utm_source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    utm_medium: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    utm_campaign: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    utm_content: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    utm_term: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # IDs de tracking específicos
    gclid: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    fbclid: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Informações do veículo (específico para revenda)
    veiculo_interesse: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Observações gerais
    observacoes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps de controle
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relacionamentos
    attributions = relationship("AttributionLink", back_populates="deal")
    
    def __repr__(self) -> str:
        return f"<CRMDeal {self.id} - {self.vendedor} - {self.status.value}>"

