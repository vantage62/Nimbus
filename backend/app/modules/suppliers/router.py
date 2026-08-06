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
from app.modules.suppliers.schemas import SupplierCreate, SupplierUpdate, SupplierResponse
from app.modules.suppliers.crud import supplier_crud

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

async def resolve_business(
    x_business_id: UUID = Header(...),
    current_user: User = Depends(get_current_active_user)
) -> UUID:
    return await get_current_business(x_business_id, current_user)

@router.post("/", response_model=SupplierResponse, status_code=201)
async def create_supplier(
    obj_in: SupplierCreate,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await supplier_crud.create(db, obj_in=obj_in, business_id=business_id)

@router.get("/", response_model=PaginatedResponse[SupplierResponse])
async def list_suppliers(
    query: Annotated[CommonQueryParams, Depends()],
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await supplier_crud.get_multi_paginated(
        db, pagination=query.pagination, sorting=query.sorting, search=query.search, business_id=business_id
    )

@router.get("/{id}", response_model=SupplierResponse)
async def get_supplier(
    id: UUID,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    supplier = await supplier_crud.get(db, id=id, business_id=business_id)
    if not supplier:
        raise NimbusException(status_code=404, message="Supplier not found", code="NOT_FOUND")
    return supplier

@router.put("/{id}", response_model=SupplierResponse)
async def update_supplier(
    id: UUID,
    obj_in: SupplierUpdate,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    supplier = await supplier_crud.get(db, id=id, business_id=business_id)
    if not supplier:
        raise NimbusException(status_code=404, message="Supplier not found", code="NOT_FOUND")
    return await supplier_crud.update(db, db_obj=supplier, obj_in=obj_in)

@router.delete("/{id}", response_model=SuccessResponse)
async def delete_supplier(
    id: UUID,
    business_id: Annotated[UUID, Depends(resolve_business)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    supplier = await supplier_crud.remove(db, id=id, business_id=business_id)
    if not supplier:
        raise NimbusException(status_code=404, message="Supplier not found", code="NOT_FOUND")
    return SuccessResponse(message="Supplier deleted successfully")
