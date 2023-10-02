from typing import Type
import pytest
from sqlalchemy.engine import Engine
from modules.base.model import BaseModel
from modules.base.repository import BaseRepository
from modules.db.services import DbServices
from sqlmodel import SQLModel
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import os
import sqlalchemy
from datetime import datetime

TEST_DB_PATH = 'test.db'
TEST_DB_URI = f'sqlite:///{TEST_DB_PATH}'




class Product(BaseModel, table=True):
     name:str
     category:str

'''
class ProductRepository(BaseRepository[Product]):
    def __init__(self, db_services: DbServices = None) -> None:
        super().__init__(Product, db_services)
'''

class MockDbServices(DbServices):
    def get_engine(self) -> Engine:

        engine = create_engine(
            TEST_DB_URI,
            connect_args={"check_same_thread": False},
            #poolclass=StaticPool,
            echo=True
        )
        
        return engine



@pytest.fixture
def repository():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    db_services = MockDbServices()
    engine = db_services.get_engine()

    SQLModel.metadata.create_all(engine)

    return BaseRepository(Product, db_services) #ProductRepository(db_services)


def test_create(repository):
    item = Product(id=1,name="Demo",category="Food")
    item = repository.create(item)

    assert item.id == 1

def test_read(repository):
    item = Product(id=1,name="Demo",category="Food")
    item = repository.create(item)
    items = repository.read()

    assert len(items) == 1 and items[0].id == 1

def test_read__deleted(repository):
    item = Product(id=1,name="Demo",category="Food", deleted_at=datetime.utcnow())
    item = repository.create(item)
    items = repository.read(include_deleted=True)

    assert len(items) == 1 and items[0].id == 1

def test_read__filter(repository):
    item = Product(id=1,name="Demo",category="Food")
    item = repository.create(item)
    items = repository.read([Product.category == 'Food'])

    assert len(items) == 1 and items[0].id == 1

def test_read__filter_not_found(repository):
    item = Product(id=1,name="Demo",category="Food")
    item = repository.create(item)
    items = repository.read([Product.category == 'Food'])

    assert len(items) == 1 and items[0].id == 1

def test_update(repository):
    item = Product(id=1,name="Demo",category="Food")
    item = repository.create(item)

    item = Product(name="Vegetable", category='Food 2')
    repository.updateById(item, 1)
    items = repository.read([Product.category == 'Food 2'])

    assert len(items) == 1 and \
            items[0].id == 1 and \
            items[0].category == 'Food 2' and \
            items[0].name == "Vegetable"

def test_update__not_found(repository):
    item = Product(name="Vegetable", category='Food 2')
    with pytest.raises(Exception):
        repository.updateById(item, 2)

def test_delete(repository):
    item = Product(id=1,name="Demo",category="Food")
    item = repository.create(item)

    repository.deleteById(1)
    results = repository.read([])
    assert len([item for item in results if item.id != 1]) == 0

def test_delete__hard(repository):
    item = Product(id=1,name="Demo",category="Food")
    item = repository.create(item)

    repository.deleteById(1, soft_delete = False)
    results = repository.read([], include_deleted=True)
    assert len([item for item in results if item.id != 1]) == 0


def test_delete__not_found(repository):
    with pytest.raises(Exception):
        repository.deleteById(2)

def test_count(repository):
    item = Product(id=1,name="Demo",category="Food")
    item = repository.create(item)

    assert repository.count() == 1

def test_count__deleted(repository):
    item = Product(id=1,name="Demo",category="Food", deleted_at=datetime.utcnow())
    item = repository.create(item)

    assert repository.count(include_deleted=True) == 1
