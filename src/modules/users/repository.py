from __future__ import annotations
from .models import User
from typing import List, Type
from sqlmodel import Session, select
from sqlalchemy import func
from ..db.services import DbServices
from sqlalchemy.orm import Query
from passlib.context import CryptContext
from ..base.repository import BaseRepository
from sqlmodel import or_
from typing import Any
from ..password.services import PaswordServices

class UsersRepository(BaseRepository[User]):
    _password_services:PaswordServices

    def __init__(self,
                 db_services: DbServices = None,
                 password_services:PaswordServices = None
                 ) -> None:
        self._password_services = password_services if password_services != None else PaswordServices()
        super().__init__(User, db_services)

    def create(self, item: User) -> User:
        item.password = self._password_services.hash_password(item.password)
        return super().create(item)

    def readByUsernameOrEmail(self, usernameOrEmail:str) -> User | None:
        results = self.read([or_(User.email == usernameOrEmail,User.username == usernameOrEmail)])
        if len(results) == 0: return None
        return results[0]