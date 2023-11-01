from fastapi import APIRouter
from .controller import ProductsController
from .models import Product
from ..pagination.models import PaginationResult
from typing import List

router = APIRouter(
    prefix='/products'
)

controller = ProductsController()

router.add_api_route('/', controller.read, methods=['GET'], response_model=PaginationResult[Product])
router.add_api_route('/', controller.create, methods=['POST'])

