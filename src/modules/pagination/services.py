from .models import PaginationResult
from typing import List, TypeVar, Generic
import math

T = TypeVar("T")

class PaginationServices():
    def get_offset(self, page:int, limit:int):
        return (page - 1) * limit

    def get_pages_count(
            self, 
            count:int, 
            limit:int
        ) -> int:
        return math.ceil(count / limit)