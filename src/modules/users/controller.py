from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from .repository import UsersRepository
from .model import User, LoginDTO
from .services import UsersServices
from ..pagination.services import PaginationServices
from ..pagination.model import PaginationResult
from sqlmodel import or_
from typing import Annotated
import os



class UsersController:
    _services:UsersServices
    _repository:UsersRepository

    def __init__(self, repository:UsersRepository = None, services:UsersServices = None) -> None:
        self._repository = UsersRepository() if repository == None else repository
        self._services = UsersServices() if services == None else services

    def demo(self, user:Annotated[User, Depends(UsersServices.check_authentication)]):
        return "A"

    def get_token(self, data:Annotated[OAuth2PasswordRequestForm, Depends()]):
        user = self._services.authenticate_user(data.username, data.password)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self._services.create_access_token(user)
        return {'access_token':access_token,'token_type':'bearer'}
 
    def create(self, item:User):
        return self._repository.create(item)