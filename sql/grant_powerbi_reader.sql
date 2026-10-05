-- Run as a PostgreSQL administrator while connected to weather_etl.
-- Create the login once, then set its password with: \password powerbi_reader
CREATE ROLE powerbi_reader LOGIN;
GRANT CONNECT ON DATABASE weather_etl TO powerbi_reader;
GRANT USAGE ON SCHEMA bi TO powerbi_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA bi TO powerbi_reader;
ALTER DEFAULT PRIVILEGES FOR ROLE weather_app IN SCHEMA bi
    GRANT SELECT ON TABLES TO powerbi_reader;
