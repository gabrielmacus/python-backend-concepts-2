from fastapi import APIRouter

from modules.base.repository import BaseRepository
from .repository import ProductsRepository
from .models import Product
from ..pagination.services import PaginationServices
from ..pagination.models import PaginationResult
from ..base.controller import BaseController
from sqlmodel import or_
from sqlalchemy.sql.operators import is_


class ProductsController(BaseController[Product]): # pragma: no cover
    def __init__(self, 
                 repository: ProductsRepository = None, 
                 pagination_services: PaginationServices = None) -> None: 
        repository = ProductsRepository() if repository == None else repository 
        super().__init__(repository, pagination_services)
'''
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
        #query = or_(is_(price_from, None), Product.price <= price_to), \
        #        or_(price_from is None, Product.price >= price_from),\
        #        or_(description is None, Product.description.ilike(f'%{description}%'))
        query = []
        if price_from != None:
            query.append(Product.price <= price_from)
        if price_to != None:
            query.append(Product.price >= price_from)
        if description != None:
            query.append(Product.description.ilike(f'%{description}%'))
        
        
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
'''