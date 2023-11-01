import pytest
from typing import Type
from modules.db.services import DbServices
from modules.users.services import UsersServices
from modules.users.models import User, TokenType
from fastapi.security import SecurityScopes
from fastapi import HTTPException, status
import time_machine
from datetime import datetime, timedelta
from jose import jwt, JWTError
from tests.mock_db_services import MockDbServices
from sqlmodel import SQLModel
from modules.base.repository import BaseRepository
from modules.users.repository import UsersRepository
from jose import jwt
@pytest.fixture
def repository():
    db_services = MockDbServices()
    engine = db_services.get_engine()

    SQLModel.metadata.create_all(engine)

    return UsersRepository(db_services=db_services)


def test_check_authentication__valid_token(repository, monkeypatch):
    monkeypatch.setenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '10')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_SECRET', 'ihasd123')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_ALGORITHM', 'HS256')

    monkeypatch.setenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES', '20')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_SECRET', 'qwertyuio')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_ALGORITHM', 'HS256')

    user = User(id=1,username="johndoe",email="johndoe@user.com",password="123456")
    repository.create(user)

    services = UsersServices(
        repository=repository
    )

    dt = datetime(2020,1,1,0,0,0)
    with time_machine.travel(dt):
        
        token = services.create_access_token(
            user,
            ['products.read','products.create'])
        
        
        auth_user = UsersServices.check_authentication(
            SecurityScopes(['products.read','products.create']),
            token,
            TokenType.ACCESS,
            repository=repository
        )

        assert auth_user.username == user.username
        assert auth_user.email == user.email
        assert hasattr(auth_user, 'password') == False

       
def test_check_authentication__invalid_token(repository, monkeypatch):
    monkeypatch.setenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '10')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_SECRET', 'ihasd123')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_ALGORITHM', 'HS256')

    monkeypatch.setenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES', '20')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_SECRET', 'qwertyuio')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_ALGORITHM', 'HS256')

    user = User(id=1,username="johndoe",email="johndoe@user.com",password="123456")
    repository.create(user)

    dt = datetime(2020,1,1,0,0,0)
    with time_machine.travel(dt):
        
        with pytest.raises(HTTPException) as ex:
            UsersServices.check_authentication(
                SecurityScopes(['products.read','products.create']),
                'invalid token',
                TokenType.ACCESS,
                repository=repository
            )
            
        assert ex.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert ex.value.headers ==  {"WWW-Authenticate":'Bearer scope="products.read products.create"'}
         
def test_check_authentication__token_without_username(repository, monkeypatch):
    monkeypatch.setenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '10')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_SECRET', 'ihasd123')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_ALGORITHM', 'HS256')

    monkeypatch.setenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES', '20')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_SECRET', 'qwertyuio')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_ALGORITHM', 'HS256')

    user = User(id=1,username="johndoe",email="johndoe@user.com",password="123456")
    repository.create(user)

    dt = datetime(2020,1,1,0,0,0)
    with time_machine.travel(dt):
        token = jwt.encode({},'ihasd123',algorithm='HS256')
        
        with pytest.raises(HTTPException) as ex:
            UsersServices.check_authentication(
                SecurityScopes(['products.read','products.create']),
                token,
                TokenType.ACCESS,
                repository=repository
            )
            
        assert ex.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert ex.value.headers ==  {"WWW-Authenticate":'Bearer scope="products.read products.create"'}
            
        
        