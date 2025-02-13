import os
from typing import Any, Optional
from .interfaces.config import IConfig

class Config(IConfig):
    def __init__(self):
        self._config = {
            'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URL', 'postgresql://postgres:Condor92!@localhost:5432/autos_db'),
            'DEBUG': os.getenv('DEBUG', 'False').lower() in ['true', '1', 't'],
            'TESTING': os.getenv('TESTING', 'False').lower() in ['true', '1', 't'],
            'SECRET_KEY': os.getenv('SECRET_KEY', 'your-secret-key-here'),
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        }

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def get_database_url(self) -> str:
        return self._config['SQLALCHEMY_DATABASE_URI']

    def get_debug_mode(self) -> bool:
        return self._config['DEBUG']

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return self.get_database_url()

    @property
    def DEBUG(self) -> bool:
        return self.get_debug_mode()

    @property
    def TESTING(self) -> bool:
        return self.get('TESTING')

    @property
    def SECRET_KEY(self) -> str:
        return self.get('SECRET_KEY')

    @property
    def SQLALCHEMY_TRACK_MODIFICATIONS(self) -> bool:
        return self.get('SQLALCHEMY_TRACK_MODIFICATIONS') 