from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Annotated

from app.database.session import get_db
from app.modules.auth.dependencies import get_current_active_user, get_current_business
from app.api.dependencies.query import CommonQueryParams
from app.modules.auth.models import User
from app.core.schemas import PaginatedResponse, SuccessResponse
from app.core.exceptions.base import NimbusException
from app.modules.sales.schemas import SaleCreate, SaleResponse
from app.modules.sales.crud import sale_crud
from app.modules.sales import service

router = APIRouter(prefix="/sales", tags=["sales"])

async def resolve_business(
    x_business_id: UUID = Header(...),
    current_user: User = Depends(get_current_active_user)
) -> UUID:
    return await get_current_business(x_business_id, current_user)

@router.post("/", response_model=SaleResponse, status_code=201)
async def create_sale(
    obj_in: SaleCreate,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.create_sale(db, obj_in, business_id)

@router.get("/", response_model=PaginatedResponse[SaleResponse])
async def list_sales(
    query: Annotated[CommonQueryParams, Depends()],
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await sale_crud.get_multi_paginated(
        db, pagination=query.pagination, sorting=query.sorting, search=query.search, business_id=business_id
    )

@router.get("/{id}", response_model=SaleResponse)
async def get_sale(
    id: UUID,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    sale = await sale_crud.get(db, id=id, business_id=business_id)
    if not sale:
        raise NimbusException(status_code=404, message="Sale not found", code="NOT_FOUND")
    return sale

@router.delete("/{id}", response_model=SuccessResponse)
async def delete_sale(
    id: UUID,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # In a real app we might reverse the inventory movement when deleting a sale.
    # For now, just soft delete the sale.
    sale = await sale_crud.remove(db, id=id, business_id=business_id)
    if not sale:
        raise NimbusException(status_code=404, message="Sale not found", code="NOT_FOUND")
    return SuccessResponse(message="Sale deleted successfully")
