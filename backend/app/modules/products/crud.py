from app.database.crud import BaseCRUD
from app.modules.products.models import Product

class CRUDProduct(BaseCRUD[Product]):
    def __init__(self):
        super().__init__(Product, searchable_fields=["sku", "name"], sortable_fields=["name", "sku", "selling_price", "created_at"])

product_crud = CRUDProduct()
