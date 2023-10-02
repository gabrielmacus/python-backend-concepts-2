from .model import Product
from ..db.services import DbServices
from ..base.repository import BaseRepository

class ProductsRepository(BaseRepository[Product]):

    def __init__(self, db_services: DbServices = None) -> None: 
        super().__init__(Product, db_services)
    