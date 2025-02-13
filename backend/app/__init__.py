from .factory import AppFactory
from .config import Config

app = AppFactory.create_app(Config())