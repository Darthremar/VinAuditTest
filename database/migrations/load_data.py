import pandas as pd
from sqlalchemy import create_engine
from ...backend.config import Config  # Actualiza la ruta de importación
import psycopg2
from io import StringIO
import argparse

# Database connection configuration
DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI

# Default CSV file path
default_file_path = 'C:/Users/USER/OneDrive/Proyectos Personales/VinAuditTest/database/NEWTEST-inventory-listing-2022-08-17.txt'

# Argument parser for command line arguments
parser = argparse.ArgumentParser(description='Load data from a CSV file into the database.')
parser.add_argument('file_path', nargs='?', default=default_file_path, type=str, help='The path to the CSV file to load.')
args = parser.parse_args()

# Create a database connection
engine = create_engine(DATABASE_URI)

# Use COPY to load data quickly
def copy_from_stringio(conn, df, table):
    """
    Use PostgreSQL's COPY method to load data from a DataFrame.
    """
    # Create an in-memory buffer
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False, sep='|')
    buffer.seek(0)

    cursor = conn.cursor()
    try:
        cursor.copy_from(buffer, table, sep='|')
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error copying data: {e}")
    finally:
        cursor.close()

# Process the CSV file in chunks
chunksize = 10000  # Adjust the chunk size as needed
with psycopg2.connect(DATABASE_URI) as conn:
    for chunk in pd.read_csv(args.file_path, delimiter='|', chunksize=chunksize):
        copy_from_stringio(conn, chunk, 'cars')

print("Data loaded successfully.") 