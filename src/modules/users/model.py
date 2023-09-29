from ..base.model import BaseModel
from pydantic import BaseModel as PydanticModel
from sqlalchemy import Text,Column
from sqlmodel import Field,Column
from pydantic import EmailStr
from enum import Enum

# https://dev.to/izabelakowal/some-ideas-on-how-to-implement-dtos-in-python-be3
class UserDTO(BaseModel):
    username:str
    email:EmailStr

class User(UserDTO, table=True):
    password:str

class LoginDTO(PydanticModel):
    access_token:str
    refresh_token:str
    token_type:str

class TokenDTO(PydanticModel):
    token:str
    token_type:str

class TokenType(Enum):
    ACCESS = 0
    REFRESH = 1