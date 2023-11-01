from abc import ABC,abstractmethod
from typing import TypeVar,Generic, List

T = TypeVar("T")

class IBaseRepository(ABC, Generic[T]):

    @abstractmethod
    def create(self, item:T) -> T:
        pass

    @abstractmethod
    def read(
            self, 
            query = None,
            limit:int = None, 
            offset:int = None,
            include_deleted:bool = False
            ) -> List[T]:
        pass

    @abstractmethod
    def updateById(self,updatedItem:T, id:int):
        pass

    @abstractmethod
    def deleteById(self, id:int, soft_delete:bool = True):
        pass

    @abstractmethod
    def count(self, 
            query = None,
            include_deleted:bool = False) -> int:
        pass