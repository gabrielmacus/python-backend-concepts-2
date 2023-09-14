from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from modules.products.router import router as products_router

app = FastAPI(openapi_tags=[
    {
        'name':'products',
        'description':'DEMO',
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    }
])
app.include_router(products_router)

