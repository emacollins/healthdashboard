-- Grant usage on the schema
GRANT USAGE ON SCHEMA activity TO eric;

-- Grant all privileges on all tables in the schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA activity TO eric;

-- Grant all privileges on all sequences in the schema
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA activity TO eric;

-- Grant all privileges on all functions in the schema
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA activity TO eric;

-- Grant future use to eric
ALTER DEFAULT PRIVILEGES IN SCHEMA activity GRANT ALL PRIVILEGES ON TABLES TO eric;
ALTER DEFAULT PRIVILEGES IN SCHEMA activity GRANT ALL PRIVILEGES ON SEQUENCES TO eric;
ALTER DEFAULT PRIVILEGES IN SCHEMA activity GRANT ALL PRIVILEGES ON FUNCTIONS TO eric;