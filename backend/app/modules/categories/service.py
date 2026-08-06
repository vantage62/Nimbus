from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.modules.categories.crud import category_crud
from app.modules.categories.schemas import CategoryCreate, CategoryUpdate
from app.core.exceptions.base import NimbusException

async def create_category(db: AsyncSession, obj_in: CategoryCreate, business_id: UUID):
    if obj_in.parent_id:
        parent = await category_crud.get(db, id=obj_in.parent_id, business_id=business_id)
        if not parent:
            raise NimbusException(status_code=400, message="Parent category not found in this business", code="BAD_REQUEST")
            
    return await category_crud.create(db, obj_in=obj_in, business_id=business_id)

async def update_category(db: AsyncSession, id: UUID, business_id: UUID, obj_in: CategoryUpdate):
    category = await category_crud.get(db, id=id, business_id=business_id)
    if not category:
        raise NimbusException(status_code=404, message="Category not found", code="NOT_FOUND")
        
    if obj_in.parent_id:
        if obj_in.parent_id == id:
            raise NimbusException(status_code=400, message="Category cannot be its own parent", code="BAD_REQUEST")
        parent = await category_crud.get(db, id=obj_in.parent_id, business_id=business_id)
        if not parent:
            raise NimbusException(status_code=400, message="Parent category not found", code="BAD_REQUEST")
            
    return await category_crud.update(db, db_obj=category, obj_in=obj_in)
