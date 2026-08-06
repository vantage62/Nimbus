from app.database.crud import BaseCRUD
from app.modules.suppliers.models import Supplier

class CRUDSupplier(BaseCRUD[Supplier]):
    def __init__(self):
        super().__init__(Supplier, searchable_fields=["name", "contact_email"], sortable_fields=["name", "created_at"])

supplier_crud = CRUDSupplier()
