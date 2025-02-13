from flask import Flask

def create_app(config_class=None):
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)
    # Register blueprints and other setup
    return app