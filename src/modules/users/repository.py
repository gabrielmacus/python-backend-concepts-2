from .model import User
from typing import List
from sqlmodel import Session, select
from sqlalchemy import func
from ..db.services import DbServices
from sqlalchemy.orm import Query
from passlib.context import CryptContext



class  UsersRepository:
    def __init__(self) -> None:
        pass

    def create(self, item:User):
        item.password = self._services.hash_password(item.password)
        
        with Session(DbServices().get_engine()) as session:
            session.add(item)
            session.commit()
            session.refresh(item)
        return item

    def read(
            self, 
            query = None,
            limit:int = None, 
            offset:int = None
            ) -> List[User]:
        with Session(DbServices().get_engine()) as session:
            statement = select(User) \
                .where(*query) \
                .limit(limit) \
                .offset(offset)
            
            results = session.exec(statement)
            items = results.all()
        return items
    
    def count(self, query = None) -> int:
        with Session(DbServices().get_engine()) as session:
            # Not optimized (slow) -> session.query(Product).count()
            count_result = session.query(func.count(User.id)).where(*query).scalar()
        return count_result
        
