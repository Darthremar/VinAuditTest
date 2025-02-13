from flask import Flask
from .routes.routes import main
from .config import Config

def create_app(config_class):
    app = Flask(__name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')
    app.config.from_object(config_class)
    app.register_blueprint(main)
    return app

if __name__ == '__main__':
    app = create_app(Config)
    app.run(debug=True) 