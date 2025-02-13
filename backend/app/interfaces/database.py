from abc import ABC, abstractmethod
from typing import Any, List, Optional, Generator
from sqlalchemy.orm import Session

class IDatabase(ABC):
    @abstractmethod
    def query(self, *args, **kwargs):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_session(self) -> Generator[Session, None, None]:
        pass

    @abstractmethod
    def init_app(self, app: Any) -> None:
        pass

    @abstractmethod
    def create_all(self) -> None:
        pass 