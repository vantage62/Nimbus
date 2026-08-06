from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from datetime import datetime

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Must be at least 8 characters long.")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    email_verified: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class BusinessMembershipResponse(BaseModel):
    business_id: UUID
    role_id: UUID | None
    
    model_config = ConfigDict(from_attributes=True)

class RoleResponse(BaseModel):
    id: UUID
    name: str
    
    model_config = ConfigDict(from_attributes=True)

class CurrentUserResponse(BaseModel):
    user: UserResponse
    memberships: list[BusinessMembershipResponse]
    roles: list[RoleResponse]
