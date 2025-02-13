from flask import Flask
from typing import Optional
from .config import Config
from .database import Database
from .routes.routes import main as main_blueprint

class AppFactory:
    @staticmethod
    def create_app(config: Optional[Config] = None) -> Flask:
        app = Flask(__name__)
        
        # Configuración
        if config is None:
            config = Config()
        app.config.from_object(config)

        # Inicializar base de datos
        db = Database(config)
        db.init_app(app)

        # Registrar blueprints
        app.register_blueprint(main_blueprint)

        return app 