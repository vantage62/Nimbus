from app.database.crud import BaseCRUD
from app.modules.business.models import Business, BusinessMembership
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

class CRUDBusiness(BaseCRUD[Business]):
    def __init__(self):
        super().__init__(Business, searchable_fields=["name", "slug"], sortable_fields=["name", "created_at", "updated_at"])

class CRUDBusinessMembership(BaseCRUD[BusinessMembership]):
    def __init__(self):
        super().__init__(BusinessMembership, sortable_fields=["created_at"])
        
    async def get_membership(self, db: AsyncSession, user_id: UUID, business_id: UUID) -> BusinessMembership | None:
        query = select(self.model).where(
            self.model.user_id == user_id, 
            self.model.business_id == business_id
        )
        result = await db.execute(query)
        return result.scalars().first()

business_crud = CRUDBusiness()
membership_crud = CRUDBusinessMembership()
