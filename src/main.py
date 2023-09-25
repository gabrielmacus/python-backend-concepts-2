from typing import Annotated

from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from modules.products.router import router as products_router
from modules.users.router import router as users_router

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(products_router)
app.include_router(users_router)