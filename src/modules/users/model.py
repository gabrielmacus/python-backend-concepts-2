from ..base.model import BaseModel
from pydantic import BaseModel as PydanticModel
from sqlalchemy import Text,Column
from sqlmodel import Field,Column
from pydantic import EmailStr

# https://dev.to/izabelakowal/some-ideas-on-how-to-implement-dtos-in-python-be3
class UserDTO(BaseModel):
    username:str
    email:EmailStr

class User(UserDTO, table=True):
    password:str

class LoginDTO(PydanticModel):
    password:str
    emailOrUsername:str

class TokenDTO(PydanticModel):
    access_token:str
    token_type:str
