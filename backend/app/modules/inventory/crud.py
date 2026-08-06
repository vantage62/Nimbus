from app.database.crud import BaseCRUD
from app.modules.inventory.models import Inventory, StockMovement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

class CRUDInventory(BaseCRUD[Inventory]):
    def __init__(self):
        super().__init__(Inventory, sortable_fields=["quantity", "available_quantity", "created_at"])
        
    async def get_by_product_and_store(self, db: AsyncSession, product_id: UUID, store_id: UUID | None, business_id: UUID) -> Inventory | None:
        query = select(self.model).where(
            self.model.business_id == business_id,
            self.model.product_id == product_id,
            self.model.store_id == store_id,
            self.model.deleted_at.is_(None)
        )
        result = await db.execute(query)
        return result.scalars().first()

class CRUDStockMovement(BaseCRUD[StockMovement]):
    def __init__(self):
        super().__init__(StockMovement, sortable_fields=["created_at"])

inventory_crud = CRUDInventory()
stock_movement_crud = CRUDStockMovement()
