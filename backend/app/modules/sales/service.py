from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.modules.sales.crud import sale_crud
from app.modules.sales.schemas import SaleCreate
from app.core.exceptions.base import NimbusException
from app.modules.inventory.crud import inventory_crud, stock_movement_crud
from app.modules.products.crud import product_crud

async def create_sale(db: AsyncSession, obj_in: SaleCreate, business_id: UUID):
    # Validate product exists
    product = await product_crud.get(db, id=obj_in.product_id, business_id=business_id)
    if not product:
        raise NimbusException(status_code=400, message="Product not found", code="BAD_REQUEST")
        
    total_amount = (obj_in.unit_price * obj_in.quantity) - obj_in.discount
    if total_amount < 0:
        raise NimbusException(status_code=400, message="Total amount cannot be negative", code="BAD_REQUEST")
        
    # Deduct Inventory
    inventory = await inventory_crud.get_by_product_and_store(db, obj_in.product_id, obj_in.store_id, business_id)
    if not inventory:
        raise NimbusException(status_code=400, message="Insufficient stock.", code="BAD_REQUEST")
        
    new_quantity = inventory.quantity - obj_in.quantity
    new_available = inventory.available_quantity - obj_in.quantity
    if new_quantity < 0 or new_available < 0:
        raise NimbusException(status_code=400, message="Insufficient stock to complete sale.", code="BAD_REQUEST")
        
    await inventory_crud.update(
        db, 
        db_obj=inventory, 
        obj_in={"quantity": new_quantity, "available_quantity": new_available},
        commit=False
    )
    
    # Create StockMovement
    movement_data = {
        "business_id": business_id,
        "product_id": obj_in.product_id,
        "store_id": obj_in.store_id,
        "movement_type": "Sale",
        "quantity_change": -obj_in.quantity,
        "notes": "Generated from sale"
    }
    await stock_movement_crud.create(db, obj_in=movement_data, business_id=business_id, commit=False)
    
    # Create Sale Record
    sale_data = obj_in.model_dump()
    sale_data["total_amount"] = total_amount
    sale = await sale_crud.create(db, obj_in=sale_data, business_id=business_id, commit=False)
    
    await db.commit()
    await db.refresh(sale)
        
    return sale
