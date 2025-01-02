-- Add migration script here
-- SQL file to create tables with named unique constraints

-- Create the users table with named unique constraints on the username and email fields
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE
);

-- Create the activity_types table
CREATE TABLE activity_types (
    id SERIAL PRIMARY KEY,
    activity_name TEXT NOT NULL,
    CONSTRAINT unique_activity_name UNIQUE (activity_name)
);

-- Create the units table
CREATE TABLE units (
    id SERIAL PRIMARY KEY,
    unit_name TEXT NOT NULL,
    CONSTRAINT unique_unit_name UNIQUE (unit_name)
);

-- Create the source_table with a named unique constraint on the name field
CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    source_name TEXT NOT NULL,
    source_version TEXT,
    device_name TEXT,
    device_manufacturer TEXT,
    device_model TEXT,
    device_hardware TEXT,
    device_software TEXT,
    CONSTRAINT unique_source UNIQUE (source_name, source_version, device_name, device_manufacturer, device_model, device_hardware, device_software)
);

-- Create the fact_table
CREATE TABLE facts (
    id BIGSERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    activity_type_id INT NOT NULL REFERENCES activity_types(id),
    unit_id INT NOT NULL REFERENCES units(id),
    source_id INT NOT NULL REFERENCES sources(id),
    creation_ts TIMESTAMPTZ NOT NULL,
    start_ts TIMESTAMPTZ NOT NULL,
    end_ts TIMESTAMPTZ NOT NULL,
    value FLOAT NOT NULL,
    CONSTRAINT unique_fact UNIQUE (user_id, activity_type_id, unit_id, source_id, creation_ts)
);

-- Create the summary_table with appropriate unique constraints
-- (Add unique constraints as needed based on your CSV extract structure)
CREATE TABLE summary (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    creation_date DATE NOT NULL,
    active_energy_burned FLOAT,
    active_energy_burned_goal FLOAT,
    active_energy_burned_unit_id INT REFERENCES units(id),
    move_time FLOAT,
    move_time_goal FLOAT,
    exercise_minutes FLOAT,
    exercise_minutes_goal FLOAT,
    stand_hours FLOAT,
    stand_hours_goal FLOAT,
    CONSTRAINT unique_summary UNIQUE (user_id, creation_date)
);

-- Example of INSERT statement with ON CONFLICT clause to avoid insertion on unique constraint violation
-- INSERT INTO user_table (name, email) VALUES ('John Doe', 'john.doe@example.com')
-- ON CONFLICT ON CONSTRAINT unique_user DO NOTHING;


