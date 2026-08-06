from app.database.crud import BaseCRUD
from app.modules.sales.models import Sale

class CRUDSale(BaseCRUD[Sale]):
    def __init__(self):
        super().__init__(Sale, sortable_fields=["sale_date", "total_amount", "created_at"])

sale_crud = CRUDSale()
