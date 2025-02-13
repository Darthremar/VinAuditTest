-- Begin transaction to improve performance by disabling auto-commit
BEGIN;

-- Database Information
-- Database: autos_db
-- User: admin
-- Host: localhost
-- Port: 5432

-- Create tables if they do not exist
CREATE TABLE IF NOT EXISTS car_basic_info (
    vin TEXT PRIMARY KEY,
    year INTEGER NULL,
    make TEXT NULL,
    model TEXT NULL,
    trim TEXT NULL
);

CREATE TABLE IF NOT EXISTS dealer_info (
    id SERIAL PRIMARY KEY,
    vin TEXT NOT NULL,
    dealer_name TEXT NULL,
    dealer_street TEXT NULL,
    dealer_city TEXT NULL,
    dealer_state TEXT NULL,
    dealer_zip TEXT NULL
);

CREATE TABLE IF NOT EXISTS listing_details (
    id SERIAL PRIMARY KEY,
    vin TEXT NOT NULL,
    listing_price NUMERIC NULL,
    listing_mileage INTEGER NULL,
    listing_status TEXT NULL,
    first_seen_date DATE NULL,
    last_seen_date DATE NULL,
    dealer_vdp_last_seen_date DATE NULL
);

CREATE TABLE IF NOT EXISTS vehicle_specs (
    id SERIAL PRIMARY KEY,
    vin TEXT NOT NULL,
    style TEXT NULL,
    driven_wheels TEXT NULL,
    engine TEXT NULL,
    fuel_type TEXT NULL,
    exterior_color TEXT NULL,
    interior_color TEXT NULL
);

CREATE TABLE IF NOT EXISTS vehicle_status (
    id SERIAL PRIMARY KEY,
    vin TEXT NOT NULL,
    used BOOLEAN NOT NULL,
    certified BOOLEAN NULL
);

CREATE TABLE IF NOT EXISTS seller_info (
    id SERIAL PRIMARY KEY,
    vin TEXT NOT NULL,
    seller_website TEXT NULL
);

-- Temporarily disable constraints and indexes to speed up data loading
ALTER TABLE car_basic_info SET UNLOGGED;
ALTER TABLE dealer_info SET UNLOGGED;
ALTER TABLE listing_details SET UNLOGGED;
ALTER TABLE vehicle_specs SET UNLOGGED;
ALTER TABLE vehicle_status SET UNLOGGED;
ALTER TABLE seller_info SET UNLOGGED;

-- Disable write-ahead logging to improve insertion speed
SET synchronous_commit = OFF;
SET session_replication_role = replica;

-- Load data using COPY (much faster than INSERT)
COPY car_basic_info FROM 'C:/Users/USER/OneDrive/Proyectos Personales/VinAuditTest/database/NEWTEST-inventory-listing-2022-08-17.txt' 
WITH (FORMAT CSV, DELIMITER '|', HEADER TRUE, NULL '', QUOTE '"');
COPY dealer_info FROM 'C:/Users/USER/OneDrive/Proyectos Personales/VinAuditTest/database/NEWTEST-inventory-listing-2022-08-17.txt' 
WITH (FORMAT CSV, DELIMITER '|', HEADER TRUE, NULL '', QUOTE '"');
COPY listing_details FROM 'C:/Users/USER/OneDrive/Proyectos Personales/VinAuditTest/database/NEWTEST-inventory-listing-2022-08-17.txt' 
WITH (FORMAT CSV, DELIMITER '|', HEADER TRUE, NULL '', QUOTE '"');
COPY vehicle_specs FROM 'C:/Users/USER/OneDrive/Proyectos Personales/VinAuditTest/database/NEWTEST-inventory-listing-2022-08-17.txt' 
WITH (FORMAT CSV, DELIMITER '|', HEADER TRUE, NULL '', QUOTE '"');
COPY vehicle_status FROM 'C:/Users/USER/OneDrive/Proyectos Personales/VinAuditTest/database/NEWTEST-inventory-listing-2022-08-17.txt' 
WITH (FORMAT CSV, DELIMITER '|', HEADER TRUE, NULL '', QUOTE '"');
COPY seller_info FROM 'C:/Users/USER/OneDrive/Proyectos Personales/VinAuditTest/database/NEWTEST-inventory-listing-2022-08-17.txt' 
WITH (FORMAT CSV, DELIMITER '|', HEADER TRUE, NULL '', QUOTE '"');

-- Restore constraints and indexes
ALTER TABLE car_basic_info SET LOGGED;
ALTER TABLE dealer_info SET LOGGED;
ALTER TABLE listing_details SET LOGGED;
ALTER TABLE vehicle_specs SET LOGGED;
ALTER TABLE vehicle_status SET LOGGED;
ALTER TABLE seller_info SET LOGGED;

-- Reindex the tables to improve performance
REINDEX TABLE car_basic_info;
REINDEX TABLE dealer_info;
REINDEX TABLE listing_details;
REINDEX TABLE vehicle_specs;
REINDEX TABLE vehicle_status;
REINDEX TABLE seller_info;

-- Optimize the tables after import
ANALYZE car_basic_info;
VACUUM ANALYZE car_basic_info;
ANALYZE dealer_info;
VACUUM ANALYZE dealer_info;
ANALYZE listing_details;
VACUUM ANALYZE listing_details;
ANALYZE vehicle_specs;
VACUUM ANALYZE vehicle_specs;
ANALYZE vehicle_status;
VACUUM ANALYZE vehicle_status;
ANALYZE seller_info;
VACUUM ANALYZE seller_info;

-- Restore write settings
SET synchronous_commit = ON;
SET session_replication_role = DEFAULT;

-- Commit the transaction
COMMIT;
