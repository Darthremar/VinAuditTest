import os

class Config:
    DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://admin:yourpassword@localhost/autos_db') 