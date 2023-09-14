from fastapi import APIRouter
from .repository import ProductsRepository
from .model import Product
from ..pagination.services import PaginationServices
from ..pagination.model import PaginationResult

router = APIRouter(
    prefix='/products'
)

class ProductsController:
    _repository:ProductsRepository
    _pagination_services:PaginationServices
    
    def __init__(
            self, 
            repository:ProductsRepository = None,
            pagination_services:PaginationServices = None
        ) -> None:
        self._repository = ProductsRepository() if repository == None else repository
        self._pagination_services = PaginationServices() if pagination_services == None else pagination_services

    def create(self, item:Product):
        return self._repository.create(item)
    
    def read(
            self,
            price_from:float = None,
            price_to:float = None,
            description:str = None,
            
            page:int = 1, 
            limit:int = 20,
    ) -> PaginationResult[Product]:
        # https://stackoverflow.com/questions/20363836/postgresql-ilike-query-with-sqlalchemy
        query = price_to == None or Product.price <= price_to, \
                price_from == None or Product.price >= price_from,\
                description == None or Product.description.ilike(f'%{description}%')


        count = self._repository.count(query)
        offset = self._pagination_services.get_offset(page, limit)
        items = self._repository.read(
            query,
            limit,
            offset)
        pages_count = self._pagination_services.get_pages_count(
            count, 
            limit, 
            items)

        return PaginationResult(
            count=count, 
            page=page, 
            pages_count=pages_count, 
            items=items
        )