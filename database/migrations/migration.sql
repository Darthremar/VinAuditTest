-- Desactivar COMMIT en cada operación para mejorar el rendimiento
BEGIN;

-- Información de la base de datos
-- Base de datos: autos_db
-- Usuario: admin
-- Host: localhost
-- Puerto: 5432

-- Deshabilitar restricciones e índices temporalmente
ALTER TABLE cars SET UNLOGGED;

-- Crear la tabla si no existe
CREATE TABLE IF NOT EXISTS cars (
    vin TEXT PRIMARY KEY,
    year INTEGER NOT NULL,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    trim TEXT,
    dealer_name TEXT NOT NULL,
    dealer_street TEXT,
    dealer_city TEXT NOT NULL,
    dealer_state TEXT NOT NULL,
    dealer_zip TEXT,
    listing_price NUMERIC NULL,
    listing_mileage INTEGER NULL,
    used BOOLEAN NOT NULL,
    certified BOOLEAN NOT NULL,
    style TEXT NULL,
    driven_wheels TEXT NULL,
    engine TEXT NULL,
    fuel_type TEXT NULL,
    exterior_color TEXT NULL,
    interior_color TEXT NULL,
    seller_website TEXT NULL,
    first_seen_date DATE NOT NULL,
    last_seen_date DATE NOT NULL,
    dealer_vdp_last_seen_date DATE NULL,
    listing_status TEXT NULL
);

-- Desactivar logs de escritura para mejorar velocidad de inserción
SET synchronous_commit = OFF;
SET session_replication_role = replica;

-- Cargar datos usando COPY (mucho más rápido que INSERT)
COPY cars FROM '/ruta/del/archivo/cars.csv' 
WITH (FORMAT CSV, DELIMITER '|', HEADER TRUE, NULL '', QUOTE '"');

-- Restaurar restricciones e índices
ALTER TABLE cars SET LOGGED;

-- Reindexar la tabla para mejorar el rendimiento
REINDEX TABLE cars;

-- Optimizar la tabla después de la importación
ANALYZE cars;
VACUUM ANALYZE cars;

-- Restaurar configuración de escritura
SET synchronous_commit = ON;
SET session_replication_role = DEFAULT;

-- Confirmar la transacción
COMMIT;
