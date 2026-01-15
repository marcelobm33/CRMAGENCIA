"""
Schemas para IA Analista
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field


class AcaoSugerida(BaseModel):
    """Uma ação sugerida pela IA"""
    acao: str
    tipo: str = Field(..., pattern="^(imediata|teste|otimizacao|analise)$")
    prioridade: Optional[int] = None


class AIRecommendationCreate(BaseModel):
    """Schema para criar recomendação"""
    escopo: str
    prioridade: str
    titulo: str
    insight: str
    explicacao: str
    acoes_sugeridas: List[AcaoSugerida]
    hipotese: Optional[str] = None
    metrica_alvo: Optional[str] = None
    impacto_esperado: Optional[str] = None
    como_medir: Optional[str] = None
    contexto_dados: Optional[dict] = None


class AIRecommendationResponse(BaseModel):
    """Schema de resposta para recomendação"""
    id: UUID
    data: datetime
    escopo: str
    prioridade: str
    titulo: str
    insight: str
    explicacao: str
    acoes_sugeridas: List[dict]
    hipotese: Optional[str]
    metrica_alvo: Optional[str]
    impacto_esperado: Optional[str]
    como_medir: Optional[str]
    status: str
    notas_usuario: Optional[str]
    resultado_obtido: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AIRecommendationUpdate(BaseModel):
    """Schema para atualizar recomendação"""
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|done|dismissed|testing)$")
    notas_usuario: Optional[str] = None
    resultado_obtido: Optional[str] = None


class AIRecommendationListResponse(BaseModel):
    """Lista de recomendações"""
    items: List[AIRecommendationResponse]
    total: int
    pendentes: int
    em_progresso: int


class AIAnalysisRequest(BaseModel):
    """Request para gerar análise manual"""
    periodo_dias: int = Field(default=7, ge=1, le=90)
    focos: Optional[List[str]] = None  # Ex: ["campanha", "vendedor", "crm"]


class AIAnalysisSummary(BaseModel):
    """Resumo da análise da IA"""
    periodo_analisado: str
    total_recomendacoes: int
    criticas: int
    oportunidades: int
    problemas: int
    resumo_executivo: str

