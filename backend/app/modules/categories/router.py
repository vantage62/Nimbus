from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Annotated

from app.database.session import get_db
from app.modules.auth.dependencies import get_current_active_user, get_current_business
from app.api.dependencies.query import CommonQueryParams
from app.modules.auth.models import User
from app.core.schemas import PaginatedResponse, SuccessResponse
from app.modules.categories.schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from app.modules.categories.crud import category_crud
from app.modules.categories import service

router = APIRouter(prefix="/categories", tags=["categories"])

async def resolve_business(
    x_business_id: UUID = Header(...),
    current_user: User = Depends(get_current_active_user)
) -> UUID:
    return await get_current_business(x_business_id, current_user)

@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    obj_in: CategoryCreate,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.create_category(db, obj_in, business_id)

@router.get("/", response_model=PaginatedResponse[CategoryResponse])
async def list_categories(
    query: Annotated[CommonQueryParams, Depends()],
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await category_crud.get_multi_paginated(
        db, pagination=query.pagination, sorting=query.sorting, search=query.search, business_id=business_id
    )

@router.get("/{id}", response_model=CategoryResponse)
async def get_category(
    id: UUID,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    category = await category_crud.get(db, id=id, business_id=business_id)
    if not category:
        from app.core.exceptions.base import NimbusException
        raise NimbusException(status_code=404, message="Category not found", code="NOT_FOUND")
    return category

@router.put("/{id}", response_model=CategoryResponse)
async def update_category(
    id: UUID,
    obj_in: CategoryUpdate,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.update_category(db, id, business_id, obj_in)

@router.delete("/{id}", response_model=SuccessResponse)
async def delete_category(
    id: UUID,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    category = await category_crud.remove(db, id=id, business_id=business_id)
    if not category:
        from app.core.exceptions.base import NimbusException
        raise NimbusException(status_code=404, message="Category not found", code="NOT_FOUND")
    return SuccessResponse(message="Category deleted successfully")
