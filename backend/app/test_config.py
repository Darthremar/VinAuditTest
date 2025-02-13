import os

class TestConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')
    TESTING = True
    DEBUG = True 