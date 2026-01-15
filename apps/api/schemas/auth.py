"""
Schemas para autenticação
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema para criar usuário"""
    email: EmailStr
    nome: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=6)
    is_admin: bool = False


class UserResponse(BaseModel):
    """Schema de resposta para usuário"""
    id: UUID
    email: str
    nome: str
    is_active: bool
    is_admin: bool
    last_login: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Request de login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Token JWT de resposta"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # segundos


class TokenData(BaseModel):
    """Dados extraídos do token"""
    user_id: Optional[str] = None
    email: Optional[str] = None

