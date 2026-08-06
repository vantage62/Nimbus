from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.modules.business.crud import business_crud, membership_crud
from app.modules.business.schemas import BusinessCreate, BusinessUpdate, BusinessMembershipCreate, BusinessMembershipUpdate
from app.core.exceptions.base import NimbusException
from app.modules.auth.models import Role
from sqlalchemy import select

async def create_business(db: AsyncSession, obj_in: BusinessCreate, user_id: UUID):
    # Check if slug exists
    query = select(business_crud.model).where(business_crud.model.slug == obj_in.slug)
    result = await db.execute(query)
    if result.scalars().first():
        raise NimbusException(status_code=409, message="Business with this slug already exists", code="CONFLICT")

    # Get Owner role
    role_query = select(Role).where(Role.name == "owner")
    role_result = await db.execute(role_query)
    owner_role = role_result.scalars().first()
    
    # Create business
    business = await business_crud.create(db, obj_in=obj_in, commit=False)
    
    # Create membership
    mem_in = BusinessMembershipCreate(user_id=user_id, role_id=owner_role.id if owner_role else None)
    await membership_crud.create(db, obj_in=mem_in.model_dump() | {"business_id": business.id}, commit=False)
    
    await db.commit()
    await db.refresh(business)
        
    return business

async def update_business(db: AsyncSession, id: UUID, obj_in: BusinessUpdate):
    business = await business_crud.get(db, id=id)
    if not business:
        raise NimbusException(status_code=404, message="Business not found", code="NOT_FOUND")
        
    if obj_in.slug and obj_in.slug != business.slug:
        query = select(business_crud.model).where(business_crud.model.slug == obj_in.slug)
        result = await db.execute(query)
        if result.scalars().first():
            raise NimbusException(status_code=409, message="Business with this slug already exists", code="CONFLICT")
            
    return await business_crud.update(db, db_obj=business, obj_in=obj_in)

async def invite_member(db: AsyncSession, business_id: UUID, obj_in: BusinessMembershipCreate):
    existing = await membership_crud.get_membership(db, obj_in.user_id, business_id)
    if existing:
        raise NimbusException(status_code=409, message="User is already a member", code="CONFLICT")
        
    # In a real app we'd send an email invite. Here we just create the membership directly.
    return await membership_crud.create(db, obj_in=obj_in.model_dump() | {"business_id": business_id})

async def remove_member(db: AsyncSession, business_id: UUID, user_id: UUID):
    existing = await membership_crud.get_membership(db, user_id, business_id)
    if not existing:
        raise NimbusException(status_code=404, message="Membership not found", code="NOT_FOUND")
        
    return await membership_crud.remove(db, id=existing.id, hard_delete=True)

async def update_member_role(db: AsyncSession, business_id: UUID, user_id: UUID, obj_in: BusinessMembershipUpdate):
    existing = await membership_crud.get_membership(db, user_id, business_id)
    if not existing:
        raise NimbusException(status_code=404, message="Membership not found", code="NOT_FOUND")
        
    return await membership_crud.update(db, db_obj=existing, obj_in=obj_in)
