from typing import Type
import pytest
from sqlalchemy.engine import Engine
from modules.base.model import BaseModel
from modules.base.repository import BaseRepository
from modules.pagination.services import PaginationServices
from modules.pagination.models import PaginationResult
from sqlmodel import SQLModel
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import os


TEST_DB_PATH = 'test.db'
TEST_DB_URI = f'sqlite:///{TEST_DB_PATH}'

os.environ['DB_CONNECTION_STRING'] = TEST_DB_URI



def test_get_offset__1():
    services = PaginationServices()
    assert 0 == services.get_offset(1, 20)


def test_get_offset__2():
    services = PaginationServices()
    assert 20 == services.get_offset(2, 20)


def test_get_offset__3():
    services = PaginationServices()
    assert 60 == services.get_offset(3, 30)

def test_get_pages_count__1():
    services = PaginationServices()
    assert services.get_pages_count(1000,20) == 50

def test_get_pages_count__2():
    services = PaginationServices()
    assert services.get_pages_count(934,30) == 32