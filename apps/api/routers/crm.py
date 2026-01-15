"""
Router de CRM (Deals/Negócios)
"""
import csv
import io
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import User
from models.crm import CRMDeal, DealStatus
from schemas.crm import (
    CRMDealCreate,
    CRMDealUpdate,
    CRMDealResponse,
    CRMDealListResponse,
    CRMImportResult
)
from routers.auth import get_current_user

router = APIRouter()


@router.get("/deals", response_model=CRMDealListResponse)
async def list_deals(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    vendedor: Optional[str] = None,
    search: Optional[str] = None,
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista deals com paginação e filtros
    """
    query = select(CRMDeal)
    
    # Aplicar filtros
    if status_filter:
        query = query.where(CRMDeal.status == DealStatus(status_filter))
    
    if vendedor:
        query = query.where(CRMDeal.vendedor.ilike(f"%{vendedor}%"))
    
    if search:
        query = query.where(
            or_(
                CRMDeal.nome_cliente.ilike(f"%{search}%"),
                CRMDeal.telefone.ilike(f"%{search}%"),
                CRMDeal.email.ilike(f"%{search}%"),
                CRMDeal.veiculo_interesse.ilike(f"%{search}%")
            )
        )
    
    if data_inicio:
        query = query.where(CRMDeal.data_criacao >= data_inicio)
    
    if data_fim:
        query = query.where(CRMDeal.data_criacao <= data_fim)
    
    # Contar total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Aplicar paginação
    query = query.order_by(CRMDeal.data_criacao.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    deals = result.scalars().all()
    
    return CRMDealListResponse(
        items=[CRMDealResponse.model_validate(d) for d in deals],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )


@router.get("/deals/{deal_id}", response_model=CRMDealResponse)
async def get_deal(
    deal_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna um deal específico
    """
    result = await db.execute(
        select(CRMDeal).where(CRMDeal.id == deal_id)
    )
    deal = result.scalar_one_or_none()
    
    if not deal:
        raise HTTPException(status_code=404, detail="Deal não encontrado")
    
    return deal


@router.post("/deals", response_model=CRMDealResponse, status_code=status.HTTP_201_CREATED)
async def create_deal(
    deal_data: CRMDealCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo deal
    """
    deal = CRMDeal(
        **deal_data.model_dump(exclude_unset=True),
        status=DealStatus(deal_data.status)
    )
    
    if deal_data.data_criacao:
        deal.data_criacao = deal_data.data_criacao
    
    db.add(deal)
    await db.commit()
    await db.refresh(deal)
    
    return deal


@router.patch("/deals/{deal_id}", response_model=CRMDealResponse)
async def update_deal(
    deal_id: UUID,
    deal_data: CRMDealUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza um deal
    """
    result = await db.execute(
        select(CRMDeal).where(CRMDeal.id == deal_id)
    )
    deal = result.scalar_one_or_none()
    
    if not deal:
        raise HTTPException(status_code=404, detail="Deal não encontrado")
    
    update_data = deal_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == "status" and value:
            setattr(deal, field, DealStatus(value))
        else:
            setattr(deal, field, value)
    
    await db.commit()
    await db.refresh(deal)
    
    return deal


@router.delete("/deals/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deal(
    deal_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove um deal
    """
    result = await db.execute(
        select(CRMDeal).where(CRMDeal.id == deal_id)
    )
    deal = result.scalar_one_or_none()
    
    if not deal:
        raise HTTPException(status_code=404, detail="Deal não encontrado")
    
    await db.delete(deal)
    await db.commit()


@router.post("/import", response_model=CRMImportResult)
async def import_deals(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Importa deals de um arquivo CSV
    
    O CSV deve ter as colunas:
    - vendedor (obrigatório)
    - valor
    - lucro_bruto
    - status (aberto/ganho/perdido)
    - motivo_perda
    - data_criacao
    - data_fechamento
    - telefone
    - email
    - nome_cliente
    - origem
    - canal
    - utm_source
    - utm_campaign
    - utm_content
    - utm_term
    - gclid
    - fbclid
    - veiculo_interesse
    - observacoes
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Arquivo deve ser CSV"
        )
    
    content = await file.read()
    
    # Detectar encoding
    try:
        text = content.decode('utf-8')
    except UnicodeDecodeError:
        text = content.decode('latin-1')
    
    reader = csv.DictReader(io.StringIO(text))
    
    total_linhas = 0
    importados = 0
    erros = []
    
    for row_num, row in enumerate(reader, start=2):  # Linha 1 é cabeçalho
        total_linhas += 1
        
        try:
            # Validar vendedor (obrigatório)
            vendedor = row.get('vendedor', '').strip()
            if not vendedor:
                raise ValueError("Campo 'vendedor' é obrigatório")
            
            # Processar status
            status_str = row.get('status', 'aberto').strip().lower()
            if status_str not in ['aberto', 'ganho', 'perdido']:
                status_str = 'aberto'
            
            # Processar datas
            data_criacao = None
            if row.get('data_criacao'):
                try:
                    data_criacao = datetime.fromisoformat(row['data_criacao'].strip())
                except:
                    data_criacao = datetime.strptime(row['data_criacao'].strip(), '%d/%m/%Y')
            
            data_fechamento = None
            if row.get('data_fechamento'):
                try:
                    data_fechamento = datetime.fromisoformat(row['data_fechamento'].strip())
                except:
                    try:
                        data_fechamento = datetime.strptime(row['data_fechamento'].strip(), '%d/%m/%Y')
                    except:
                        pass
            
            # Processar valores
            valor = 0
            if row.get('valor'):
                valor_str = row['valor'].replace('R$', '').replace('.', '').replace(',', '.').strip()
                valor = float(valor_str) if valor_str else 0
            
            lucro = 0
            if row.get('lucro_bruto'):
                lucro_str = row['lucro_bruto'].replace('R$', '').replace('.', '').replace(',', '.').strip()
                lucro = float(lucro_str) if lucro_str else 0
            
            # Criar deal
            deal = CRMDeal(
                vendedor=vendedor,
                valor=valor,
                lucro_bruto=lucro,
                status=DealStatus(status_str),
                motivo_perda=row.get('motivo_perda', '').strip() or None,
                data_criacao=data_criacao or datetime.utcnow(),
                data_fechamento=data_fechamento,
                telefone=row.get('telefone', '').strip() or None,
                email=row.get('email', '').strip() or None,
                nome_cliente=row.get('nome_cliente', '').strip() or None,
                origem=row.get('origem', '').strip() or None,
                canal=row.get('canal', '').strip() or None,
                utm_source=row.get('utm_source', '').strip() or None,
                utm_medium=row.get('utm_medium', '').strip() or None,
                utm_campaign=row.get('utm_campaign', '').strip() or None,
                utm_content=row.get('utm_content', '').strip() or None,
                utm_term=row.get('utm_term', '').strip() or None,
                gclid=row.get('gclid', '').strip() or None,
                fbclid=row.get('fbclid', '').strip() or None,
                veiculo_interesse=row.get('veiculo_interesse', '').strip() or None,
                observacoes=row.get('observacoes', '').strip() or None
            )
            
            db.add(deal)
            importados += 1
            
        except Exception as e:
            erros.append({
                "linha": row_num,
                "erro": str(e),
                "dados": dict(row)
            })
    
    await db.commit()
    
    return CRMImportResult(
        total_linhas=total_linhas,
        importados=importados,
        erros=len(erros),
        detalhes_erros=erros[:10]  # Limitar a 10 erros no retorno
    )


@router.get("/vendedores", response_model=List[str])
async def list_vendedores(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todos os vendedores únicos
    """
    result = await db.execute(
        select(CRMDeal.vendedor).distinct().order_by(CRMDeal.vendedor)
    )
    vendedores = [row[0] for row in result.all()]
    return vendedores


@router.get("/stats")
async def get_crm_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Estatísticas gerais do CRM
    """
    # Total de deals
    total_result = await db.execute(select(func.count(CRMDeal.id)))
    total = total_result.scalar()
    
    # Por status
    status_query = select(
        CRMDeal.status,
        func.count(CRMDeal.id)
    ).group_by(CRMDeal.status)
    status_result = await db.execute(status_query)
    status_counts = {row[0].value: row[1] for row in status_result.all()}
    
    # Valor total
    valor_result = await db.execute(
        select(func.sum(CRMDeal.valor)).where(CRMDeal.status == DealStatus.GANHO)
    )
    valor_total = valor_result.scalar() or 0
    
    # Lucro total
    lucro_result = await db.execute(
        select(func.sum(CRMDeal.lucro_bruto)).where(CRMDeal.status == DealStatus.GANHO)
    )
    lucro_total = lucro_result.scalar() or 0
    
    return {
        "total_deals": total,
        "por_status": status_counts,
        "valor_total_ganho": float(valor_total),
        "lucro_bruto_total": float(lucro_total)
    }

