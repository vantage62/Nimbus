from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select
from app.modules.products.crud import product_crud
from app.modules.products.schemas import ProductCreate, ProductUpdate
from app.core.exceptions.base import NimbusException
from app.modules.categories.crud import category_crud
from app.modules.suppliers.crud import supplier_crud

async def create_product(db: AsyncSession, obj_in: ProductCreate, business_id: UUID):
    # Validate SKU uniqueness
    query = select(product_crud.model).where(
        product_crud.model.business_id == business_id,
        product_crud.model.sku == obj_in.sku,
        product_crud.model.deleted_at.is_(None)
    )
    result = await db.execute(query)
    if result.scalars().first():
        raise NimbusException(status_code=409, message="Product with this SKU already exists", code="CONFLICT")
        
    # Validate category ownership
    if obj_in.category_id:
        cat = await category_crud.get(db, id=obj_in.category_id, business_id=business_id)
        if not cat:
            raise NimbusException(status_code=400, message="Category not found", code="BAD_REQUEST")
            
    # Validate supplier ownership
    if obj_in.supplier_id:
        sup = await supplier_crud.get(db, id=obj_in.supplier_id, business_id=business_id)
        if not sup:
            raise NimbusException(status_code=400, message="Supplier not found", code="BAD_REQUEST")
            
    return await product_crud.create(db, obj_in=obj_in, business_id=business_id)

async def update_product(db: AsyncSession, id: UUID, business_id: UUID, obj_in: ProductUpdate):
    product = await product_crud.get(db, id=id, business_id=business_id)
    if not product:
        raise NimbusException(status_code=404, message="Product not found", code="NOT_FOUND")
        
    # Validate SKU uniqueness if changing
    if obj_in.sku and obj_in.sku != product.sku:
        query = select(product_crud.model).where(
            product_crud.model.business_id == business_id,
            product_crud.model.sku == obj_in.sku,
            product_crud.model.deleted_at.is_(None)
        )
        result = await db.execute(query)
        if result.scalars().first():
            raise NimbusException(status_code=409, message="Product with this SKU already exists", code="CONFLICT")
            
    # Validate category ownership if changing
    if obj_in.category_id and obj_in.category_id != product.category_id:
        cat = await category_crud.get(db, id=obj_in.category_id, business_id=business_id)
        if not cat:
            raise NimbusException(status_code=400, message="Category not found", code="BAD_REQUEST")
            
    # Validate supplier ownership if changing
    if obj_in.supplier_id and obj_in.supplier_id != product.supplier_id:
        sup = await supplier_crud.get(db, id=obj_in.supplier_id, business_id=business_id)
        if not sup:
            raise NimbusException(status_code=400, message="Supplier not found", code="BAD_REQUEST")
            
    return await product_crud.update(db, db_obj=product, obj_in=obj_in)
