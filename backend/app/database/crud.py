from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseCRUD(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def _apply_soft_delete_filter(self, query, include_deleted: bool = False):
        if not include_deleted and hasattr(self.model, "deleted_at"):
            return query.where(self.model.deleted_at.is_(None))
        return query

    async def get(self, db: AsyncSession, id: UUID, include_deleted: bool = False) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        query = self._apply_soft_delete_filter(query, include_deleted)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> List[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        query = self._apply_soft_delete_filter(query, include_deleted)
        result = await db.execute(query)
        return list(result.scalars().all())
