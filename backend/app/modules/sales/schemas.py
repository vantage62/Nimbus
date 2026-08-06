from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from decimal import Decimal

class SaleBase(BaseModel):
    product_id: UUID
    store_id: Optional[UUID] = None
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., ge=0)
    discount: Decimal = Field(default=Decimal('0.0'), ge=0)

class SaleCreate(SaleBase):
    pass

class SaleResponse(SaleBase):
    id: UUID
    business_id: UUID
    sale_date: datetime
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
