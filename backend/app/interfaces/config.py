from abc import ABC, abstractmethod
from typing import Any, Optional

class IConfig(ABC):
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        pass

    @abstractmethod
    def get_database_url(self) -> str:
        pass

    @abstractmethod
    def get_debug_mode(self) -> bool:
        pass 