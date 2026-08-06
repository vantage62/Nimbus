from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class InventoryBase(BaseModel):
    product_id: UUID
    store_id: Optional[UUID] = None

class InventoryResponse(InventoryBase):
    id: UUID
    business_id: UUID
    quantity: int
    reserved_quantity: int
    available_quantity: int
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class StockAdjustment(BaseModel):
    product_id: UUID
    store_id: Optional[UUID] = None
    movement_type: str = Field(..., description="e.g. Initial Stock, Purchase, Sale, Return, Damage, Manual Adjustment, Restock, Transfer")
    quantity_change: int = Field(..., description="Positive for addition, negative for deduction")
    notes: Optional[str] = None

class StockMovementResponse(BaseModel):
    id: UUID
    business_id: UUID
    product_id: UUID
    store_id: Optional[UUID]
    movement_type: str
    quantity_change: int
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
