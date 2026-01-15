"""
Modelo de snapshots de KPIs
"""
import uuid
from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, DateTime, Date, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
import enum

from database import Base


class AggregationType(str, enum.Enum):
    """Tipos de agregação de KPIs"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class KPISnapshot(Base):
    """
    Snapshot de métricas agregadas
    Pré-calcula KPIs para performance do dashboard
    """
    __tablename__ = "kpi_snapshots"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    # Período
    periodo_inicio: Mapped[date] = mapped_column(Date)
    periodo_fim: Mapped[date] = mapped_column(Date)
    
    # Tipo de agregação
    agregacao: Mapped[AggregationType] = mapped_column(SQLEnum(AggregationType))
    
    # Dimensões (filtros)
    canal: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # google, meta, all
    campaign_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    vendedor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Métricas em JSON para flexibilidade
    # Exemplo de estrutura:
    # {
    #   "gasto_total": 5000.00,
    #   "impressoes": 100000,
    #   "cliques": 2000,
    #   "leads": 150,
    #   "deals_total": 100,
    #   "deals_ganhos": 30,
    #   "deals_perdidos": 50,
    #   "deals_abertos": 20,
    #   "valor_total": 500000.00,
    #   "lucro_bruto": 75000.00,
    #   "cpl": 33.33,
    #   "cpa": 166.67,
    #   "taxa_conversao": 30.0,
    #   "roas": 10.0,
    #   "ticket_medio": 16666.67,
    #   "motivos_perda": {"preco": 20, "sem_retorno": 15, "outro": 15}
    # }
    metricas: Mapped[dict] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
    
    def __repr__(self) -> str:
        return f"<KPISnapshot {self.periodo_inicio} - {self.periodo_fim} | {self.agregacao.value}>"

