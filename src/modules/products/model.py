from ..base.model import BaseModel
from sqlmodel import Field,Column
from sqlalchemy import Text,Column

class Product(BaseModel, table=True):
    price:float
    description:str = Field(sa_column=Column(Text(), nullable=False))