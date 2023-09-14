from sqlmodel import create_engine
from sqlalchemy.engine import Engine
import sqlmodel
import os

class DbServices():
    _engine:Engine = None
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DbServices, cls).__new__(cls)
        return cls.instance

    def get_engine(self) -> Engine:
        if self._engine == None:
            # TODO: Echo on debugonly
            self._engine = create_engine(os.getenv('DB_CONNECTION_STRING'), echo=True)
        return self._engine