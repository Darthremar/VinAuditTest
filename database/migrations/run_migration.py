import psycopg2
from backend.app.config import Config

# Database connection configuration
DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI

# Read the SQL file
with open('database/migrations/migration.sql', 'r') as file:
    sql_script = file.read()

# Connect to the database and execute the SQL script
try:
    with psycopg2.connect(DATABASE_URI) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_script)
            conn.commit()
    print("Migration executed successfully.")
except Exception as e:
    print(f"Error executing migration: {e}") 