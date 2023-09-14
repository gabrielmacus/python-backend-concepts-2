from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel,Column,Date
from sqlalchemy import BigInteger,Integer

# primary_key=True,

class BaseModel(SQLModel, table=False):
    id:Optional[int] = Field(sa_column=Column(BigInteger(), default=None, primary_key=True))
    created_at:Optional[datetime] = Field(default_factory=datetime.utcnow,nullable=False)
    updated_at:Optional[datetime] = None