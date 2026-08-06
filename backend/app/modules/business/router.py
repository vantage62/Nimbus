from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Annotated

from app.database.session import get_db
from app.modules.auth.dependencies import get_current_active_user, get_current_business
from app.api.dependencies.query import CommonQueryParams, PaginationParams, SortingParams, SearchParams
from app.modules.auth.models import User
from app.core.schemas import PaginatedResponse, SuccessResponse
from app.modules.business.schemas import (
    BusinessCreate, BusinessUpdate, BusinessResponse, 
    BusinessMembershipCreate, BusinessMembershipUpdate, BusinessMembershipResponse
)
from app.modules.business.crud import business_crud, membership_crud
from app.modules.business import service

router = APIRouter(prefix="/business", tags=["business"])

@router.post("/", response_model=BusinessResponse, status_code=201)
async def create_business(
    obj_in: BusinessCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.create_business(db, obj_in, current_user.id)

@router.get("/", response_model=PaginatedResponse[BusinessResponse])
async def list_businesses(
    query: Annotated[CommonQueryParams, Depends()],
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Depending on requirements, we could list all businesses the user is a member of.
    # For now, if superuser they see all, otherwise they see memberships.
    # We will list via membership join ideally, but for this generic example we just call get_multi_paginated.
    # Realistically we should filter by memberships if not superuser, but we'll stick to basic CRUD for now.
    user_roles = [r.name for r in current_user.roles]
    if "superuser" not in user_roles:
        business_ids = [m.business_id for m in current_user.memberships]
        return await business_crud.get_multi_paginated(
            db, pagination=query.pagination, sorting=query.sorting, search=query.search, id=business_ids
        )
    
    return await business_crud.get_multi_paginated(
        db, pagination=query.pagination, sorting=query.sorting, search=query.search
    )

@router.get("/{id}", response_model=BusinessResponse)
async def get_business(
    id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    business_id = await get_current_business(id, current_user)
    return await business_crud.get(db, id=business_id)

@router.put("/{id}", response_model=BusinessResponse)
async def update_business(
    id: UUID,
    obj_in: BusinessUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    business_id = await get_current_business(id, current_user)
    return await service.update_business(db, business_id, obj_in)

@router.delete("/{id}", response_model=SuccessResponse)
async def delete_business(
    id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    business_id = await get_current_business(id, current_user)
    await business_crud.remove(db, id=business_id)
    return SuccessResponse(message="Business deleted successfully")

# Membership routes
@router.post("/{id}/members", response_model=BusinessMembershipResponse, status_code=201)
async def invite_member(
    id: UUID,
    obj_in: BusinessMembershipCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    business_id = await get_current_business(id, current_user)
    return await service.invite_member(db, business_id, obj_in)

@router.put("/{id}/members/{user_id}", response_model=BusinessMembershipResponse)
async def update_member(
    id: UUID,
    user_id: UUID,
    obj_in: BusinessMembershipUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    business_id = await get_current_business(id, current_user)
    return await service.update_member_role(db, business_id, user_id, obj_in)

@router.delete("/{id}/members/{user_id}", response_model=SuccessResponse)
async def remove_member(
    id: UUID,
    user_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    business_id = await get_current_business(id, current_user)
    await service.remove_member(db, business_id, user_id)
    return SuccessResponse(message="Member removed successfully")
