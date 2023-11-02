import pytest
from typing import Type
from modules.db.services import DbServices
from modules.users.services import UsersServices
from modules.users.models import User, TokenType
from fastapi.security import SecurityScopes
import time_machine
from datetime import datetime, timedelta
from jose import jwt

# https://www.testim.io/blog/unit-test-vs-integration-test/
# https://docs.pytest.org/en/latest/how-to/monkeypatch.html

class MockJWTServices():
    def decode(self, token,secret,algorithms):
        return {
            'sub':'z'
        }



class MockUsersRepository():
    users = [
        User(id=1,email="user_2@user.com",username="user2",password="123456"),
        User(id=2,email="user@user.com",username="user",password="654321")
    ]
    def readByUsernameOrEmail(self, usernameOrEmail):
        results = [user for user in self.users if user.username == usernameOrEmail or user.email == usernameOrEmail]
        if len(results) == 0: return None
        return results[0]
    
    def read(self, query):
        print(query)
        return []

class MockPasswordContext():
    def hash(self, password:str):
        return password
    def verify(self, secret:str, hash:str):
        return secret == hash

@pytest.fixture
def services():
    return UsersServices(
        repository=MockUsersRepository(),
        password_context=MockPasswordContext())

def test_authenticate_user__username(services):
    user = services.authenticate_user('user','654321')
    assert user != None and user.id == 2

def test_authenticate_user__email(services):
    user = services.authenticate_user('user_2@user.com', '123456')
    assert user != None and user.id == 1

def test_authenticate_user__existing_username_wrong_pass(services):
    user = services.authenticate_user('user','111111')
    assert user == None

def test_authenticate_user__existing_email_wrong_pass(services):
    user = services.authenticate_user('user@user.com','111111')
    assert user == None

def test_hash_password(services):
    hash = services.hash_password('123456')
    assert hash == '123456'

def test_create_token__access(services, monkeypatch):
    monkeypatch.setenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '10')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_SECRET', 'ihasd123')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_ALGORITHM', 'HS256')

    monkeypatch.setenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES', '20')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_SECRET', 'qwertyuio')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_ALGORITHM', 'HS256')

    dt = datetime(2020,1,1,0,0,0)
    with time_machine.travel(dt):

        token = services.create_access_token(
            User(id=1,username="johndoe",email="johndoe@user.com",password="123456"),
            ['products.read','products.create'])
        
        payload = jwt.get_unverified_claims(token)
        headers = jwt.get_unverified_headers(token)
        
        assert headers['alg'] == 'HS256'
        assert payload['scopes'] == ['products.read','products.create']
        assert payload['sub'] == 'johndoe'
        assert datetime.utcfromtimestamp(payload['exp']) == dt + timedelta(minutes=10)
        assert datetime.utcfromtimestamp(payload['iat']) == dt

def test_create_token__refresh(services, monkeypatch):
    monkeypatch.setenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '10')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_SECRET', 'ihasd123')
    monkeypatch.setenv('JWT_ACCESS_TOKEN_ALGORITHM', 'HS256')

    monkeypatch.setenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES', '20')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_SECRET', 'qwertyuio')
    monkeypatch.setenv('JWT_REFRESH_TOKEN_ALGORITHM', 'HS256')

    dt = datetime(2020,1,1,0,0,0)
    with time_machine.travel(dt):

        token = services.create_refresh_token(
            User(id=1,username="johndoe",email="johndoe@user.com",password="123456"))
        
        payload = jwt.get_unverified_claims(token)
        headers = jwt.get_unverified_headers(token)
        
        assert headers['alg'] == 'HS256'
        assert payload['scopes'] == []
        assert payload['sub'] == 'johndoe'
        assert datetime.utcfromtimestamp(payload['exp']) == dt + timedelta(minutes=20)
        assert datetime.utcfromtimestamp(payload['iat']) == dt

def test_check_scopes(services):
    result = services.check_scopes(
        ["products:read"], 
        SecurityScopes(["products:read"])
        )

    assert result == True

def test_check_scopes__multi(services):
    result = services.check_scopes(
        ["products:create","products:read", "users:read",], 
        SecurityScopes(["products:read", "products:create"])
    )

    assert result == True

def test_check_scopes__wildcard(services):
    result = services.check_scopes(
        ["products:*"], 
        SecurityScopes(["products:read"])
    )

    assert result == True

def test_check_scopes__negation(services):
    result = services.check_scopes(
        ["products:*", "!products:create"], 
        SecurityScopes(["products:create"])
    )

    assert result == False


def test_check_scopes__negation_2(services):
    result = services.check_scopes(
        ["users.read", "products:*", "!products:create"], 
        SecurityScopes(["users:read","products:create"])
    )

    assert result == False


def test_check_scopes__negation_3(services):
    result = services.check_scopes(
        ["products:*", "!products:create"], 
        SecurityScopes(["products:read"])
    )

    assert result == True

def test_check_scopes__unauthorized(services):
    result = services.check_scopes(
        ["products:create"], 
        SecurityScopes(["products:read"])
        )

    assert result == False


def test_check_scopes__empty_unauthorized(services):
    result = services.check_scopes(
        [], 
        SecurityScopes(["products:read"])
        )

    assert result == False

def test_check_scopes__empty_authorized_1(services):
    result = services.check_scopes(
        [], 
        SecurityScopes([])
        )

    assert result == True


def test_check_scopes__empty_authorized_2(services):
    result = services.check_scopes(
        ["products:*"], 
        SecurityScopes([])
        )

    assert result == True