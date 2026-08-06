from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.modules.inventory.crud import inventory_crud, stock_movement_crud
from app.modules.inventory.schemas import StockAdjustment
from app.core.exceptions.base import NimbusException
from app.modules.products.crud import product_crud

async def adjust_stock(db: AsyncSession, obj_in: StockAdjustment, business_id: UUID):
    # Validate product belongs to business
    product = await product_crud.get(db, id=obj_in.product_id, business_id=business_id)
    if not product:
        raise NimbusException(status_code=400, message="Product not found", code="BAD_REQUEST")
        
    # In a real app we'd validate store_id too.
    
    inventory = await inventory_crud.get_by_product_and_store(db, obj_in.product_id, obj_in.store_id, business_id)
    if not inventory:
        # Create new inventory record if it doesn't exist
        if obj_in.quantity_change < 0:
            raise NimbusException(status_code=400, message="Cannot deduct stock: inventory record does not exist and would become negative", code="BAD_REQUEST")
        
        inventory = await inventory_crud.create(
            db, 
            obj_in={"product_id": obj_in.product_id, "store_id": obj_in.store_id, "quantity": 0, "available_quantity": 0}, 
            business_id=business_id,
            commit=False
        )
        
    new_quantity = inventory.quantity + obj_in.quantity_change
    if new_quantity < 0:
        raise NimbusException(status_code=400, message=f"Insufficient stock. Current: {inventory.quantity}, Requested change: {obj_in.quantity_change}", code="BAD_REQUEST")
        
    new_available = inventory.available_quantity + obj_in.quantity_change
    if new_available < 0:
        raise NimbusException(status_code=400, message="Insufficient available stock.", code="BAD_REQUEST")
        
    # Update Inventory
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
        "movement_type": obj_in.movement_type,
        "quantity_change": obj_in.quantity_change,
        "notes": obj_in.notes
    }
    movement = await stock_movement_crud.create(db, obj_in=movement_data, business_id=business_id, commit=False)
    
    await db.commit()
    await db.refresh(movement)
    
    return movement
