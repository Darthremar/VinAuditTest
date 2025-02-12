import os

class Config:
    DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://postgres:Condor92!@localhost:5432/autos_db') 
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'options': '-csearch_path=public'
        }
    }
    SQLALCHEMY_BINDS = {
        'autos_db': DATABASE_URI
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

