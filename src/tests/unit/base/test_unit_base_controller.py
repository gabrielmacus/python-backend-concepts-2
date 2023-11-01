from typing import List, Type
import pytest
from sqlalchemy.engine import Engine
from modules.base.model import BaseModel
from modules.pagination.models import PaginationResult
from modules.base.repository import BaseRepository
from modules.base.controller import BaseController
from modules.db.services import DbServices
from sqlmodel import SQLModel
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import os
import sqlalchemy
from datetime import datetime


class Product(BaseModel, table=False):
     name:str
     category:str


class ProductsRepository(BaseRepository):
    items = [
        Product(name="Vegetable",category="Food"),
        Product(name="Chocolate",category="Food"),
        Product(name="Meat",category="Food"),
        Product(name="Donuts",category="Food"),
        Product(name="Honey",category="Food")
    ]
    
    def __init__(self) -> None:
        pass
    
    def read(self, 
             query=None, 
             limit: int = None, 
             offset: int = None, 
             include_deleted: bool = False) -> List:
        

        if offset != None:
            items = self.items[offset:limit + offset]
        else:
            items = self.items[:limit]

        return items
    
    def create(self, item: any) -> any:
        item.id = len(self.items) + 1
        self.items.append(item)
        return item

    def count(self, query=None, include_deleted: bool = False) -> int:
        return len(self.items)

@pytest.fixture
def controller():

    repository = ProductsRepository()
    controller = BaseController(repository)

    return controller


def test_read(controller):
    result = controller.read(limit = 3, page = 1)

    assert len(result.items) == 3 and\
        result.count == 5 and \
        result.page == 1 and \
        result.pages_count == 2

def test_read__page_2(controller):
    result = controller.read(limit = 3, page = 2)

    assert len(result.items) == 2 and\
        result.count == 5 and \
        result.page == 2 and \
        result.pages_count == 2
    
def test_create(controller):
    item = controller.create(Product(
        category="Furniture",
        name="Oven"
    ))
    result = controller.read(limit = 20, page = 1)
    assert item.id == 6 and len([i for i in result.items if i.id == 6]) == 1