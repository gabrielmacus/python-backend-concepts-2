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


TEST_DB_PATH = 'test.db'
TEST_DB_URI = f'sqlite:///{TEST_DB_PATH}'

os.environ['DB_CONNECTION_STRING'] = TEST_DB_URI

def test_create_engine():
    assert isinstance(DbServices().get_engine(), Engine) == True