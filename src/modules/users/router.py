from fastapi import APIRouter, Response
from .controller import UsersController
from .models import User, UserDTO, LoginData
from ..pagination.models import PaginationResult
from typing import List

router = APIRouter(
    prefix='/users'
)

controller = UsersController()

#router.add_api_route('/', controller.read, methods=['GET'], response_model=PaginationResult[UserDTO])
router.add_api_route('/', controller.create, methods=['POST'])
router.add_api_route('/token', controller.get_token, methods=['POST'], response_model=LoginData)
router.add_api_route('/token/refresh', controller.refresh_token, methods=['POST'])

