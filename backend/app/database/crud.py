from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from sqlalchemy import select, func, asc, desc, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import StaleDataError
from app.database.base import Base
from app.api.dependencies.query import PaginationParams, SortingParams, SearchParams
from app.core.schemas import PaginatedResponse
from app.core.exceptions.base import NimbusException
import math

ModelType = TypeVar("ModelType", bound=Base)

class BaseCRUD(Generic[ModelType]):
    def __init__(
        self, 
        model: Type[ModelType],
        searchable_fields: List[str] = None,
        sortable_fields: List[str] = None
    ):
        self.model = model
        self.searchable_fields = searchable_fields or []
        self.sortable_fields = sortable_fields or ["created_at", "updated_at"]

    def _apply_soft_delete_filter(self, query, include_deleted: bool = False):
        if not include_deleted and hasattr(self.model, "deleted_at"):
            return query.where(self.model.deleted_at.is_(None))
        return query

    def _apply_business_isolation(self, query, business_id: Optional[UUID]):
        if business_id and hasattr(self.model, "business_id"):
            return query.where(self.model.business_id == business_id)
        return query

    def _apply_search(self, query, search: Optional[str]):
        if search and self.searchable_fields:
            search_filters = []
            for field in self.searchable_fields:
                column = getattr(self.model, field)
                search_filters.append(cast(column, String).ilike(f"%{search}%"))
            if search_filters:
                from sqlalchemy import or_
                query = query.where(or_(*search_filters))
        return query

    def _apply_sorting(self, query, sort: Optional[str], order: str):
        if sort and sort in self.sortable_fields:
            column = getattr(self.model, sort)
            if order.lower() == "desc":
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))
        else:
            # Default fallback sort
            if hasattr(self.model, "created_at"):
                query = query.order_by(desc(self.model.created_at))
        return query

    async def get(self, db: AsyncSession, id: UUID, business_id: Optional[UUID] = None, include_deleted: bool = False) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        query = self._apply_business_isolation(query, business_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi_paginated(
        self, 
        db: AsyncSession,
        *,
        pagination: PaginationParams,
        sorting: Optional[SortingParams] = None,
        search: Optional[SearchParams] = None,
        business_id: Optional[UUID] = None,
        include_deleted: bool = False,
        **filters: Any
    ):
        query = select(self.model)
        query = self._apply_business_isolation(query, business_id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        
        if search and search.search:
            query = self._apply_search(query, search.search)
            
        # Apply exact match filters
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                column = getattr(self.model, key)
                if isinstance(value, (list, tuple, set)):
                    query = query.where(column.in_(value))
                else:
                    query = query.where(column == value)
                
        # Count total before limit/offset
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Apply Sorting
        if sorting:
            query = self._apply_sorting(query, sorting.sort, sorting.order)
        else:
            query = self._apply_sorting(query, None, "desc")
            
        # Apply Pagination
        query = query.offset(pagination.skip).limit(pagination.page_size)
        
        result = await db.execute(query)
        items = list(result.scalars().all())
        
        pages = math.ceil(total / pagination.page_size) if total > 0 else 0
        
        return PaginatedResponse(
            items=items,
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
            pages=pages
        )

    async def create(self, db: AsyncSession, *, obj_in: Any, business_id: Optional[UUID] = None, commit: bool = True) -> ModelType:
        obj_in_data = obj_in.model_dump(exclude_unset=True) if hasattr(obj_in, "model_dump") else obj_in
        if business_id and hasattr(self.model, "business_id"):
            obj_in_data["business_id"] = business_id
            
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        if commit:
            await db.commit()
            await db.refresh(db_obj)
        else:
            await db.flush()
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: ModelType, obj_in: Any, commit: bool = True) -> ModelType:
        obj_data = db_obj.__dict__
        update_data = obj_in.model_dump(exclude_unset=True) if hasattr(obj_in, "model_dump") else obj_in
        
        # Check optimistic locking version match if provided
        if hasattr(self.model, "version") and "version" in update_data:
            if update_data["version"] != db_obj.version:
                raise NimbusException(status_code=409, message="Concurrent update detected.", code="CONFLICT")
                
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        if commit:
            try:
                await db.commit()
                await db.refresh(db_obj)
            except StaleDataError:
                await db.rollback()
                raise NimbusException(status_code=409, message="Concurrent update detected.", code="CONFLICT")
        else:
            await db.flush()
            
        return db_obj

    async def remove(self, db: AsyncSession, *, id: UUID, business_id: Optional[UUID] = None, hard_delete: bool = False, commit: bool = True) -> Optional[ModelType]:
        obj = await self.get(db, id=id, business_id=business_id)
        if not obj:
            return None
            
        if not hard_delete and hasattr(self.model, "deleted_at"):
            from app.database.base import utcnow
            obj.deleted_at = utcnow()
            db.add(obj)
            if commit:
                await db.commit()
            else:
                await db.flush()
        else:
            await db.delete(obj)
            if commit:
                await db.commit()
            else:
                await db.flush()
            
        return obj
