import pandas as pd
from sqlalchemy import create_engine
from backend.app.config import Config
from backend.app.models.car_basic_info import CarBasicInfo
from backend.app.models.dealer_info import DealerInfo
from backend.app.models.listing_details import ListingDetails
from backend.app.models.vehicle_specs import VehicleSpecs
from backend.app.models.vehicle_status import VehicleStatus
from backend.app.models.seller_info import SellerInfo
from backend.app.database import Base
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

# Create tables if they do not exist
Base.metadata.create_all(engine)

# Use COPY to load data quickly
def copy_from_stringio(conn, df, table):
    """
    Use PostgreSQL's COPY method to load data from a DataFrame.
    """
    # Create an in-memory buffer
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False, sep='|', na_rep='NULL')
    buffer.seek(0)

    cursor = conn.cursor()
    try:
        cursor.copy_from(buffer, table, sep='|', null='NULL', columns=[col for col in df.columns])
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
        # Remove duplicates based on 'vin'
        chunk = chunk.drop_duplicates(subset='vin')

        # Ensure VIN does not have NaN
        chunk = chunk.dropna(subset=['vin'])

        # Convert listing_mileage to integer, handling NaN values
        chunk['listing_mileage'] = pd.to_numeric(chunk['listing_mileage'], errors='coerce').fillna(0).astype(int)

        # Convert listing_price to numeric, handling NaN values
        chunk['listing_price'] = pd.to_numeric(chunk['listing_price'], errors='coerce').fillna(0)

        # Convert date columns to datetime, handling NaN values
        date_columns = ['first_seen_date', 'last_seen_date', 'dealer_vdp_last_seen_date']
        for date_col in date_columns:
            chunk[date_col] = pd.to_datetime(chunk[date_col], errors='coerce')

        # Convert all NaN to None
        chunk = chunk.where(pd.notnull(chunk), None)

        # Load data into each table, excluding 'id'
        copy_from_stringio(conn, chunk[['vin', 'year', 'make', 'model', 'trim']], CarBasicInfo.__tablename__)
        copy_from_stringio(conn, chunk[['vin', 'dealer_name', 'dealer_street', 'dealer_city', 'dealer_state', 'dealer_zip']], DealerInfo.__tablename__)
        copy_from_stringio(conn, chunk[['vin', 'listing_price', 'listing_mileage', 'listing_status', 'first_seen_date', 'last_seen_date', 'dealer_vdp_last_seen_date']], ListingDetails.__tablename__)
        copy_from_stringio(conn, chunk[['vin', 'style', 'driven_wheels', 'engine', 'fuel_type', 'exterior_color', 'interior_color']], VehicleSpecs.__tablename__)
        copy_from_stringio(conn, chunk[['vin', 'used', 'certified']], VehicleStatus.__tablename__)
        copy_from_stringio(conn, chunk[['vin', 'seller_website']], SellerInfo.__tablename__)

print("Data loaded successfully.") 