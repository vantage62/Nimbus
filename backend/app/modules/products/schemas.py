from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from decimal import Decimal

class ProductBase(BaseModel):
    category_id: Optional[UUID] = None
    supplier_id: Optional[UUID] = None
    sku: str
    name: str
    cost_price: Decimal = Field(default=Decimal('0.0'), ge=0)
    selling_price: Decimal = Field(default=Decimal('0.0'), ge=0)
    minimum_stock: int = Field(default=0, ge=0)
    safety_stock: int = Field(default=0, ge=0)
    reorder_point: int = Field(default=0, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    category_id: Optional[UUID] = None
    supplier_id: Optional[UUID] = None
    sku: Optional[str] = None
    name: Optional[str] = None
    cost_price: Optional[Decimal] = Field(default=None, ge=0)
    selling_price: Optional[Decimal] = Field(default=None, ge=0)
    minimum_stock: Optional[int] = Field(default=None, ge=0)
    safety_stock: Optional[int] = Field(default=None, ge=0)
    reorder_point: Optional[int] = Field(default=None, ge=0)
    version: Optional[int] = None

class ProductResponse(ProductBase):
    id: UUID
    business_id: UUID
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
