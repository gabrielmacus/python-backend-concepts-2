
import pytest
from modules.users.controller import UsersController
from modules.users.repository import UsersRepository
from modules.users.models import User
from sqlmodel import SQLModel
from tests.mock_db_services import MockDbServices
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
import time_machine
from datetime import datetime, timedelta
from fastapi import HTTPException, FastAPI

from fastapi.testclient import TestClient
from main import create_app

class MockUserServices:
    def hash_password(self,secret):
        return secret[1::]
    
@pytest.fixture
def db_services():
    db_services = MockDbServices()
    engine = db_services.get_engine()
    SQLModel.metadata.create_all(engine)
    return db_services


def test_create__is_hashing(db_services, monkeypatch):
    repository = UsersRepository(
        db_services,
        services=MockUserServices()
        
    ) 
    controller = UsersController(
        repository=repository
    )
    controller.create(User(
        id=1,
        email='user@user.com',
        password='123456',
        username='user'
    ))
    result = controller.read()
    assert result.items[0].password != '123456' 

def test_get_token(db_services, monkeypatch):
    repository = UsersRepository(
        db_services
        
    ) 
    monkeypatch.setenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '10')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_SECRET', 'ihasd123')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_ALGORITHM', 'HS256')

    monkeypatch.setenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES', '20')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_SECRET', 'qwertyuio')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_ALGORITHM', 'HS256')
    
    dt = datetime(2020,1,1,0,0,0)
    with time_machine.travel(dt):
        controller = UsersController(repository=repository)
        repository.create(User(
            id=1,
            email='user@user.com',
            password='123456',
            username='user'
        ))

        data = controller.get_token(OAuth2PasswordRequestForm(username="user",password="123456"))
        
        payload = jwt.get_unverified_claims(data.access_token)
        headers = jwt.get_unverified_headers(data.access_token)

        assert headers['alg'] == 'HS256'
        #assert payload['scopes'] == ['products.read','products.create']
        assert payload['sub'] == 'user'
        assert datetime.utcfromtimestamp(payload['exp']) == dt + timedelta(minutes=10)
        assert datetime.utcfromtimestamp(payload['iat']) == dt

        payload = jwt.get_unverified_claims(data.refresh_token)
        headers = jwt.get_unverified_headers(data.refresh_token)

        assert headers['alg'] == 'HS256'
        assert payload['scopes'] == []
        assert payload['sub'] == 'user'
        assert datetime.utcfromtimestamp(payload['exp']) == dt + timedelta(minutes=20)
        assert datetime.utcfromtimestamp(payload['iat']) == dt

def test_get_token__invalid_credentials(db_services, monkeypatch):
    monkeypatch.setenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '10')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_SECRET', 'ihasd123')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_ALGORITHM', 'HS256')

    monkeypatch.setenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES', '20')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_SECRET', 'qwertyuio')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_ALGORITHM', 'HS256')
    
    repository = UsersRepository(
        db_services
    ) 

    controller = UsersController(repository=repository)
    repository.create(User(
        id=1,
        email='user@user.com',
        password='123456',
        username='user'
    ))

    with pytest.raises(HTTPException):
        controller.get_token(OAuth2PasswordRequestForm(username="user",password="111"))

def test_refresh_token(db_services, monkeypatch):
    monkeypatch.setenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '10')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_SECRET', 'ihasd123')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_ALGORITHM', 'HS256')

    monkeypatch.setenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES', '20')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_SECRET', 'qwertyuio')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_ALGORITHM', 'HS256')
    
    repository = UsersRepository(
        db_services
    ) 
    
    dt = datetime(2020,1,1,0,0,0)
    with time_machine.travel(dt):
        controller = UsersController(repository=repository)
        data = controller.refresh_token(User(
                id=1,
                email='user@user.com',
                password='123456',
                username='user'
        ))

        
        payload = jwt.get_unverified_claims(data.token)
        headers = jwt.get_unverified_headers(data.token)

        assert headers['alg'] == 'HS256'
        #assert payload['scopes'] == []
        assert payload['sub'] == 'user'
        assert datetime.utcfromtimestamp(payload['exp']) == dt + timedelta(minutes=10)
        assert datetime.utcfromtimestamp(payload['iat']) == dt

def test__token_generation_api(db_services, monkeypatch):
    monkeypatch.setenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '10')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_SECRET', 'ihasd123')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_ALGORITHM', 'HS256')

    monkeypatch.setenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES', '20')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_SECRET', 'qwertyuio')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_ALGORITHM', 'HS256')

    monkeypatch.setenv('DB_CONNECTION_STRING','sqlite:///test.db')


    dt = datetime(2020,1,1,0,0,0)
    with time_machine.travel(dt):
        repository = UsersRepository(
            db_services,  
        ) 
        repository.create(User(
            id=1,
            username="user",
            email="user@user.com",
            password="123456",
        ))
        

        app = create_app()
        client = TestClient(app)
        
        # Test invalid credentials
        response = client.post('/users/token', data={
            "username":"user",
            "password":"1111"
        })
        assert response.status_code == 401

        # Test valid credentials with email and username
        for val in ['user','user@user.com']:
            response = client.post('/users/token', data={
                "username":val,
                "password":"123456"
            })
            
            assert response.status_code == 200
            
            access_token = response.json()['access_token']
            payload = jwt.get_unverified_claims(access_token)

            assert payload['sub'] == 'user'
            assert datetime.utcfromtimestamp(payload['exp']) == dt + timedelta(minutes=10)
            assert datetime.utcfromtimestamp(payload['iat']) == dt


            refresh_token = response.json()['refresh_token']
            payload = jwt.get_unverified_claims(refresh_token)

            assert payload['sub'] == 'user'
            assert datetime.utcfromtimestamp(payload['exp']) == dt + timedelta(minutes=20)
            assert datetime.utcfromtimestamp(payload['iat']) == dt

            response = client.post('/')
            
        # Test refresh
        client = TestClient(app, cookies={
            "token":refresh_token
        })
        response = client.post('/users/token/refresh')
        assert response.status_code == 200

        # Test refresh invalid token
        client = TestClient(app, cookies={
            "token":'invalid'
        })
        response = client.post('/users/token/refresh')
        assert response.status_code == 401


'''
def test_refresh_token__api(db_services, monkeypatch):
    monkeypatch.setenv('DB_CONNECTION_STRING','sqlite:///test.db')
    app = create_app()
    client = TestClient(app)
    response = client.post('/users/token/refresh')

    assert response == 0
'''