from fastapi import Query
from dataclasses import dataclass
from typing import Optional

@dataclass
class PaginationParams:
    page: int = Query(1, ge=1, description="Page number")
    page_size: int = Query(20, ge=1, le=100, description="Items per page")
    
    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size

@dataclass
class SortingParams:
    sort: Optional[str] = Query(None, description="Field to sort by")
    order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order (asc or desc)")

@dataclass
class SearchParams:
    search: Optional[str] = Query(None, description="Search term")

from fastapi import Depends

@dataclass
class CommonQueryParams:
    pagination: PaginationParams = Depends()
    sorting: SortingParams = Depends()
    search: SearchParams = Depends()
