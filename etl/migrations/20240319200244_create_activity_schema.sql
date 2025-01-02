-- Add migration script here
-- Create the schema
CREATE SCHEMA activity;

-- Set the default search path to the new schema
ALTER DATABASE applehealth SET search_path TO activity;
