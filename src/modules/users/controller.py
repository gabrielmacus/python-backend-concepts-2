from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer

from modules.base.repository import BaseRepository
from .repository import UsersRepository
from .models import User, LoginData, TokenData
from .services import UsersServices
from ..pagination.services import PaginationServices
from ..pagination.models import PaginationResult
from ..base.controller import BaseController
from sqlmodel import or_
from typing import Annotated
import os

# https://www.reddit.com/r/node/comments/12ailfn/where_to_store_acces_and_refresh_tokens/
# https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
# https://www.stackhawk.com/blog/csrf-protection-in-fastapi/

class UsersController(BaseController[User]):
    _services:UsersServices
    _repository:UsersRepository

    def __init__(self, 
                 repository: UsersRepository = None, 
                 services: UsersServices = None,
                 pagination_services: PaginationServices = None) -> None:
        self._repository = UsersRepository() if repository == None else repository
        self._services = UsersServices() if services == None else services
        super().__init__(repository, pagination_services)


    def demo(self, 
             user:Annotated[User, 
                            Security(UsersServices.check_access_token, scopes=['users:demo'])]
            ):# pragma: no cover
        return "A"

    def get_token(self, data:Annotated[OAuth2PasswordRequestForm, Depends()]):
        user = self._services.authenticate_user(data.username, data.password)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self._services.create_access_token(user, data.scopes)
        refresh_token = self._services.create_refresh_token(user)
        return LoginData(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type='bearer'
        )
    
    def refresh_token(self, 
                          user:Annotated[User,Security(UsersServices.check_refresh_token)]):
        access_token = self._services.create_access_token(user, [])
        return TokenData(token=access_token, token_type='bearer')
 