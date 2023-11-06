from .repository import BaseRepository
from ..pagination.services import PaginationServices
from ..pagination.models import PaginationResult
from typing import Type, TypeVar,Generic
import os

T = TypeVar("T")

class BaseController(Generic[T]):
    _repository:BaseRepository
    _pagination_services:PaginationServices

    def __init__(
            self, 
            repository:BaseRepository,
            pagination_services:PaginationServices = None
        ) -> None:
        self._repository = repository
        self._pagination_services = PaginationServices() if pagination_services == None else pagination_services

    def create(self, item:T):
        return self._repository.create(item)
    
    def read(
            self,
            query:list = [],
            page:int = 1, 
            limit:int = 20,
    ) -> PaginationResult[T]:
        
        count = self._repository.count(query)
        offset = self._pagination_services.get_offset(page, limit)
        items = self._repository.read(
            query,
            limit,
            offset)
        pages_count = self._pagination_services.get_pages_count(
            count, 
            limit)

        return PaginationResult(
            count=count,
            page=page, 
            pages_count=pages_count, 
            items=items
        )