"""
Modelo de recomendações da IA Analista
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
import enum

from database import Base


class RecommendationPriority(str, enum.Enum):
    """Prioridade da recomendação"""
    CRITICAL = "critical"   # Ação imediata necessária
    HIGH = "high"           # Importante, fazer em breve
    MEDIUM = "medium"       # Pode melhorar performance
    LOW = "low"             # Otimização opcional


class RecommendationScope(str, enum.Enum):
    """Escopo/área da recomendação"""
    CAMPANHA = "campanha"
    CRIATIVO = "criativo"
    PUBLICO = "publico"
    ORCAMENTO = "orcamento"
    LANDING = "landing"
    ATENDIMENTO = "atendimento"
    FOLLOWUP = "followup"
    CRM = "crm"
    GERAL = "geral"


class RecommendationStatus(str, enum.Enum):
    """Status da recomendação"""
    PENDING = "pending"       # Aguardando ação
    IN_PROGRESS = "in_progress"  # Em andamento
    DONE = "done"             # Concluída
    DISMISSED = "dismissed"   # Descartada
    TESTING = "testing"       # Em teste A/B


class AIRecommendation(Base):
    """
    Recomendação gerada pela IA Analista
    """
    __tablename__ = "ai_recommendations"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    # Quando foi gerada
    data: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
    
    # Classificação
    escopo: Mapped[RecommendationScope] = mapped_column(SQLEnum(RecommendationScope))
    prioridade: Mapped[RecommendationPriority] = mapped_column(SQLEnum(RecommendationPriority))
    
    # Conteúdo principal
    titulo: Mapped[str] = mapped_column(String(500))
    insight: Mapped[str] = mapped_column(Text)  # O que a IA viu
    explicacao: Mapped[str] = mapped_column(Text)  # O que isso significa
    
    # Ações sugeridas (lista em JSON)
    # Exemplo:
    # [
    #   {"acao": "Pausar criativo X", "tipo": "imediata"},
    #   {"acao": "Testar novo público Y", "tipo": "teste"},
    #   {"acao": "Aumentar orçamento em 20%", "tipo": "otimizacao"}
    # ]
    acoes_sugeridas: Mapped[list] = mapped_column(JSON, default=list)
    
    # Hipótese a ser testada
    hipotese: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Métrica alvo (o que melhorar)
    metrica_alvo: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Impacto esperado
    impacto_esperado: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Como medir o resultado
    como_medir: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Status e tracking
    status: Mapped[RecommendationStatus] = mapped_column(
        SQLEnum(RecommendationStatus),
        default=RecommendationStatus.PENDING
    )
    
    # Dados de contexto quando foi gerada (para referência)
    contexto_dados: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Feedback do usuário
    notas_usuario: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Resultado após implementação
    resultado_obtido: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    def __repr__(self) -> str:
        return f"<AIRecommendation {self.titulo[:50]} - {self.prioridade.value}>"

