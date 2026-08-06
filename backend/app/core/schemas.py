from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, List, Optional, Any

T = TypeVar("T")

class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    code: str
    details: Optional[Any] = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    page: int
    page_size: int
    total: int
    pages: int

    model_config = ConfigDict(from_attributes=True)
