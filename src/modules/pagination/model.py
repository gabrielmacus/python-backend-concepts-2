from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import List, TypeVar, Generic
T = TypeVar("T")

# https://github.com/tiangolo/fastapi/issues/653#issuecomment-984509798
class PaginationResult(GenericModel, Generic[T]):
    count:int
    page:int
    pages_count:int
    items:List[T]
        