from passlib.context import CryptContext
from .model import User, TokenType
from .repository import UsersRepository
from sqlmodel import or_
from datetime import timedelta, datetime
import os
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from typing import Annotated
from fastapi import Depends,HTTPException,status, Cookie
from pydantic import ValidationError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme_refresh = OAuth2PasswordBearer(tokenUrl="token/refresh")

class UsersServices:
    _password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    _repository:UsersRepository
    
    def __init__(self, repository: UsersRepository = None) -> None:
        self._repository = UsersRepository() if repository == None else repository

    def hash_password(self, plain_password:str):
        return self._password_context.hash(plain_password)

    def authenticate_user(self, username:str, password:str):
        query = [or_(User.email == username,
            User.username == username)]
        results = self._repository.read(query)
        if len(results) == 1 and \
           self._password_context.verify(password, results[0].password) == True:
            return results[0]

        return None
            
    def create_token(self, user:User, scopes:list[str], type:TokenType):
        if type == TokenType.ACCESS:
            token_expire_minutes = os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES')
            token_secret = os.getenv('JWT_ACCESS_TOKEN_SECRET')
            token_algorithm = os.getenv('JWT_ACCESS_TOKEN_ALGORITHM')
        else:
            token_expire_minutes = os.getenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES')
            token_secret = os.getenv('JWT_REFRESH_TOKEN_SECRET')
            token_algorithm = os.getenv('JWT_REFRESH_TOKEN_ALGORITHM')  

        expires_delta = timedelta(minutes=int(token_expire_minutes))
        expiration_date = datetime.utcnow() + expires_delta
        data_to_encode = {
            "iat":datetime.utcnow(),
            "sub":user.username,
            "exp":expiration_date,
            "scopes":scopes
        }

        encoded_jwt = jwt.encode(
            data_to_encode,
            token_secret, 
            algorithm=token_algorithm
        )
        return encoded_jwt      
    
    def create_access_token(self, user:User, scopes:list[str]):
        return self.create_token(user, scopes, TokenType.ACCESS)
    
    def create_refresh_token(self, user:User):
        return self.create_token(user, [], TokenType.REFRESH)
    
    @staticmethod
    def check_refresh_token(token:Annotated[str | None, Cookie()] = None):
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"},
            )
        return UsersServices.check_authentication(
            SecurityScopes(None),
            token,
            TokenType.REFRESH)
    
    def check_access_token(security_scopes:SecurityScopes, 
                           token:Annotated[str, Depends(oauth2_scheme)]):
        return UsersServices.check_authentication(
            security_scopes,
            token,
            TokenType.ACCESS) 
    
    @staticmethod
    def check_scopes(token_scopes:list[str], security_scopes:SecurityScopes):
        pass
    
    @staticmethod
    def check_authentication(security_scopes:SecurityScopes, 
                             token:str,
                             token_type:TokenType):
        if token_type == TokenType.ACCESS:
            jwt_secret = os.getenv('JWT_ACCESS_TOKEN_SECRET')
            jwt_algorithm = os.getenv('JWT_ACCESS_TOKEN_ALGORITHM')
        else:
            jwt_secret = os.getenv('JWT_REFRESH_TOKEN_SECRET')
            jwt_algorithm = os.getenv('JWT_REFRESH_TOKEN_ALGORITHM')

        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"
        
        repository = UsersRepository()
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": authenticate_value},
        )
        
        try:
            payload = jwt.decode(
                token, 
                jwt_secret, 
                algorithms=[jwt_algorithm])
            username:str = payload.get('sub')
            if username is None:
                raise credentials_exception
            token_scopes:list[str] = payload.get("scopes", [])
        except JWTError:
            raise credentials_exception
        
        results = repository.read([User.username == username])
        if len(results) == 0:
            raise credentials_exception
        
        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    headers={"WWW-Authenticate": authenticate_value},
                )
        
        return results[0]