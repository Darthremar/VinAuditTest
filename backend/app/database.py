from typing import Generator, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.pool import QueuePool
from .interfaces.database import IDatabase
from .config import Config

# Base for models containing functions to declare types on models
Base = declarative_base()

class Database(IDatabase):
    def __init__(self, config: Config):
        self.config = config
        self.engine = create_engine(
            config.get_database_url(),
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def get_session(self) -> Generator[Session, None, None]:
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def init_app(self, app: Any) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = self.config.get_database_url()
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        Base.metadata.create_all(bind=self.engine)

    def create_all(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    def query(self, *args, **kwargs) -> Any:
        session = self.SessionLocal()
        try:
            return session.query(*args, **kwargs)
        finally:
            session.close()

    def close(self) -> None:
        self.engine.dispose()

# Instancia global de la base de datos
db = Database(Config())
SessionLocal = db.SessionLocal 