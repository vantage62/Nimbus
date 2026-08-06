from app.database.crud import BaseCRUD
from app.modules.categories.models import Category

class CRUDCategory(BaseCRUD[Category]):
    def __init__(self):
        super().__init__(Category, searchable_fields=["name", "description"], sortable_fields=["name", "created_at"])

category_crud = CRUDCategory()
