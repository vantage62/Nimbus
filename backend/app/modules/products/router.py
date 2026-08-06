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
from app.modules.products.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.modules.products.crud import product_crud
from app.modules.products import service

router = APIRouter(prefix="/products", tags=["products"])

async def resolve_business(
    x_business_id: UUID = Header(...),
    current_user: User = Depends(get_current_active_user)
) -> UUID:
    return await get_current_business(x_business_id, current_user)

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    obj_in: ProductCreate,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.create_product(db, obj_in, business_id)

@router.get("/", response_model=PaginatedResponse[ProductResponse])
async def list_products(
    query: Annotated[CommonQueryParams, Depends()],
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await product_crud.get_multi_paginated(
        db, pagination=query.pagination, sorting=query.sorting, search=query.search, business_id=business_id
    )

@router.get("/{id}", response_model=ProductResponse)
async def get_product(
    id: UUID,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    product = await product_crud.get(db, id=id, business_id=business_id)
    if not product:
        raise NimbusException(status_code=404, message="Product not found", code="NOT_FOUND")
    return product

@router.put("/{id}", response_model=ProductResponse)
async def update_product(
    id: UUID,
    obj_in: ProductUpdate,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.update_product(db, id, business_id, obj_in)

@router.delete("/{id}", response_model=SuccessResponse)
async def delete_product(
    id: UUID,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    product = await product_crud.remove(db, id=id, business_id=business_id)
    if not product:
        raise NimbusException(status_code=404, message="Product not found", code="NOT_FOUND")
    return SuccessResponse(message="Product deleted successfully")
