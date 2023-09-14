from ..base.model import BaseModel
from sqlmodel import Field, SQLModel,Column,Date
from sqlalchemy import Text,Column

class Product(BaseModel, table=True):
    price:float
    description:str = Field(sa_column=Column(Text(), nullable=False))