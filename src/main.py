from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from modules.products.router import router as products_router
from modules.users.router import router as users_router


def create_app():

    #load_dotenv()
    
    app = FastAPI()

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    app.include_router(products_router)
    app.include_router(users_router)
    return app