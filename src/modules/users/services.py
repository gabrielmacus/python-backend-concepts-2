from passlib.context import CryptContext
from .model import User
from .repository import UsersRepository
from sqlmodel import or_
from datetime import timedelta, datetime
import os
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends,HTTPException,status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
            
    def create_access_token(self, user:User):
        expires_delta = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
        expiration_date = datetime.utcnow() + expires_delta
        data_to_encode = {
            "sub":user.username,
            "exp":expiration_date
        }
        encoded_jwt = jwt.encode(data_to_encode,os.getenv('JWT_SECRET'), algorithm=os.getenv('JWT_ALGORITHM'))
        return encoded_jwt
    
    @staticmethod
    def check_authentication(token:Annotated[str, Depends(oauth2_scheme)]):
        repository = UsersRepository()

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=[os.getenv('JWT_ALGORITHM')])
            username:str = payload.get('sub')
            if str is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        results = repository.read([User.username == username])
        if len(results) == 0:
            raise credentials_exception
        
        return results[0]