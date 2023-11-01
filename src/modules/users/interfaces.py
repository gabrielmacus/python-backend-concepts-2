from ..base.interfaces import IBaseRepository
from .models import User
from abc import abstractmethod, ABC

class IUsersRepository(ABC):
    
    @abstractmethod
    def readByUsernameOrEmail(self, 
                              usernameOrEmail:str) -> User | None:
        pass