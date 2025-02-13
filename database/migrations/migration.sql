-- Begin transaction to improve performance by disabling auto-commit
BEGIN;

-- Database Information
-- Database: autos_db
-- User: admin
-- Host: localhost
-- Port: 5432

-- Create the table if it does not exist
CREATE TABLE IF NOT EXISTS cars (
    vin TEXT PRIMARY KEY,
    year INTEGER NULL,
    make TEXT NULL,
    model TEXT NULL,
    trim TEXT,
    dealer_name TEXT NULL,
    dealer_street TEXT,
    dealer_city TEXT NULL,
    dealer_state TEXT NULL,
    dealer_zip TEXT,
    listing_price NUMERIC NULL,
    listing_mileage INTEGER NULL,
    used BOOLEAN NOT NULL,
    certified BOOLEAN NULL,
    style TEXT NULL,
    driven_wheels TEXT NULL,
    engine TEXT NULL,
    fuel_type TEXT NULL,
    exterior_color TEXT NULL,
    interior_color TEXT NULL,
    seller_website TEXT NULL,
    first_seen_date DATE NULL,
    last_seen_date DATE NULL,
    dealer_vdp_last_seen_date DATE NULL,
    listing_status TEXT NULL
);

-- Temporarily disable constraints and indexes to speed up data loading
ALTER TABLE cars SET UNLOGGED;

-- Disable write-ahead logging to improve insertion speed
SET synchronous_commit = OFF;
SET session_replication_role = replica;

-- Load data using COPY (much faster than INSERT)
COPY cars FROM 'C:/Users/USER/Desktop/autos_db/database/NEWTEST-inventory-listing-2022-08-17.txt' 
WITH (FORMAT CSV, DELIMITER '|', HEADER TRUE, NULL '', QUOTE '"');

-- Restore constraints and indexes
ALTER TABLE cars SET LOGGED;

-- Reindex the table to improve performance
REINDEX TABLE cars;

-- Optimize the table after import
ANALYZE cars;
VACUUM ANALYZE cars;

-- Restore write settings
SET synchronous_commit = ON;
SET session_replication_role = DEFAULT;

-- Commit the transaction
COMMIT;
