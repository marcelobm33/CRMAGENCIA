"""
Schemas para CRM Deals
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr


class CRMDealBase(BaseModel):
    """Base schema para deals"""
    vendedor: str = Field(..., min_length=1, max_length=255)
    valor: Decimal = Field(default=Decimal("0"), ge=0)
    lucro_bruto: Decimal = Field(default=Decimal("0"))
    
    # Contato
    telefone: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    nome_cliente: Optional[str] = Field(None, max_length=255)
    
    # Origem
    origem: Optional[str] = Field(None, max_length=100)
    canal: Optional[str] = Field(None, max_length=100)
    
    # UTMs
    utm_source: Optional[str] = Field(None, max_length=255)
    utm_medium: Optional[str] = Field(None, max_length=255)
    utm_campaign: Optional[str] = Field(None, max_length=255)
    utm_content: Optional[str] = Field(None, max_length=255)
    utm_term: Optional[str] = Field(None, max_length=255)
    
    # Tracking IDs
    gclid: Optional[str] = Field(None, max_length=255)
    fbclid: Optional[str] = Field(None, max_length=255)
    
    # Específico revenda
    veiculo_interesse: Optional[str] = Field(None, max_length=255)
    observacoes: Optional[str] = None


class CRMDealCreate(CRMDealBase):
    """Schema para criar deal"""
    data_criacao: Optional[datetime] = None
    data_fechamento: Optional[datetime] = None
    status: str = Field(default="aberto", pattern="^(aberto|ganho|perdido)$")
    motivo_perda: Optional[str] = Field(None, max_length=255)


class CRMDealUpdate(BaseModel):
    """Schema para atualizar deal"""
    vendedor: Optional[str] = Field(None, max_length=255)
    valor: Optional[Decimal] = Field(None, ge=0)
    lucro_bruto: Optional[Decimal] = None
    status: Optional[str] = Field(None, pattern="^(aberto|ganho|perdido)$")
    motivo_perda: Optional[str] = Field(None, max_length=255)
    data_fechamento: Optional[datetime] = None
    telefone: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    nome_cliente: Optional[str] = Field(None, max_length=255)
    origem: Optional[str] = Field(None, max_length=100)
    canal: Optional[str] = Field(None, max_length=100)
    observacoes: Optional[str] = None


class CRMDealResponse(CRMDealBase):
    """Schema de resposta para deal"""
    id: UUID
    data_criacao: datetime
    data_fechamento: Optional[datetime]
    status: str
    motivo_perda: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CRMDealListResponse(BaseModel):
    """Lista paginada de deals"""
    items: List[CRMDealResponse]
    total: int
    page: int
    page_size: int
    pages: int


class CRMImportResult(BaseModel):
    """Resultado da importação de CSV/JSON"""
    total_linhas: int
    importados: int
    erros: int
    detalhes_erros: List[dict] = []

