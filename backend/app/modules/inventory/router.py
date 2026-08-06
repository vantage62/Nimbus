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
from app.modules.inventory.schemas import InventoryResponse, StockAdjustment, StockMovementResponse
from app.modules.inventory.crud import inventory_crud, stock_movement_crud
from app.modules.inventory import service

router = APIRouter(prefix="/inventory", tags=["inventory"])

async def resolve_business(
    x_business_id: UUID = Header(...),
    current_user: User = Depends(get_current_active_user)
) -> UUID:
    return await get_current_business(x_business_id, current_user)

@router.get("/", response_model=PaginatedResponse[InventoryResponse])
async def list_inventory(
    query: Annotated[CommonQueryParams, Depends()],
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await inventory_crud.get_multi_paginated(
        db, pagination=query.pagination, sorting=query.sorting, search=query.search, business_id=business_id
    )

@router.get("/{id}", response_model=InventoryResponse)
async def get_inventory(
    id: UUID,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    inventory = await inventory_crud.get(db, id=id, business_id=business_id)
    if not inventory:
        raise NimbusException(status_code=404, message="Inventory record not found", code="NOT_FOUND")
    return inventory

@router.post("/adjust", response_model=StockMovementResponse, status_code=201)
async def adjust_stock(
    obj_in: StockAdjustment,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.adjust_stock(db, obj_in, business_id)

@router.get("/movements", response_model=PaginatedResponse[StockMovementResponse])
async def list_stock_movements(
    query: Annotated[CommonQueryParams, Depends()],
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await stock_movement_crud.get_multi_paginated(
        db, pagination=query.pagination, sorting=query.sorting, search=query.search, business_id=business_id
    )
