from .model import Product
from typing import List
from sqlmodel import Session, select
from sqlalchemy import func
from ..db.services import DbServices
from sqlalchemy.orm import Query

class ProductsRepository:

    def __init__(self,) -> None:
        pass

    def create(self, item:Product):
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
            ) -> List[Product]:
        with Session(DbServices().get_engine()) as session:
            statement = select(Product) \
                .where(*query) \
                .limit(limit) \
                .offset(offset)

            results = session.exec(statement)
            items = results.all()
        return items
    
    def count(self, query = None) -> int:
        with Session(DbServices().get_engine()) as session:
            # Not optimized (slow) -> session.query(Product).count()
            count_result = session.query(func.count(Product.id)).where(*query).scalar()
        return count_result
        
