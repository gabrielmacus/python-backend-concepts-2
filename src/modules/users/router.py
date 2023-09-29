from fastapi import APIRouter, Response
from .controller import UsersController
from .model import User, UserDTO, LoginDTO
from ..pagination.model import PaginationResult
from typing import List

router = APIRouter(
    prefix='/users'
)

controller = UsersController()

#router.add_api_route('/', controller.read, methods=['GET'], response_model=PaginationResult[UserDTO])
router.add_api_route('/', controller.create, methods=['POST'])
router.add_api_route('/token', controller.get_token, methods=['POST'], response_model=LoginDTO)
router.add_api_route('/token/refresh', controller.refresh_token, methods=['POST'])

router.add_api_route('/demo', controller.demo, methods=['GET'])