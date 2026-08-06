from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class BusinessBase(BaseModel):
    name: str
    slug: str

class BusinessCreate(BusinessBase):
    pass

class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    version: Optional[int] = None

class BusinessResponse(BusinessBase):
    id: UUID
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BusinessMembershipCreate(BaseModel):
    user_id: UUID
    role_id: Optional[UUID] = None

class BusinessMembershipUpdate(BaseModel):
    role_id: Optional[UUID] = None

class BusinessMembershipResponse(BaseModel):
    id: UUID
    user_id: UUID
    business_id: UUID
    role_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
