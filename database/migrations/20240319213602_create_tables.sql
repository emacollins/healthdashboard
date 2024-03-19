-- Add migration script here
-- SQL file to create tables with named unique constraints

-- Create the user_table with a named unique constraint on the email field
CREATE TABLE user_table (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    CONSTRAINT unique_user UNIQUE (username, email)
);

-- Create the activity_type_table
CREATE TABLE activity_type_table (
    id SERIAL PRIMARY KEY,
    activity_name TEXT NOT NULL,
    CONSTRAINT unique_activity_name UNIQUE (activity_name)
);

-- Create the unit_table
CREATE TABLE unit_table (
    id SERIAL PRIMARY KEY,
    unit_name TEXT NOT NULL,
    CONSTRAINT unique_unit_name UNIQUE (unit_name)
);

-- Create the source_table with a named unique constraint on the name field
CREATE TABLE source_table (
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
CREATE TABLE fact_table (
    id BIGSERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES user_table(id),
    activity_type_id INT NOT NULL REFERENCES activity_type_table(id),
    unit_id INT NOT NULL REFERENCES unit_table(id),
    source_id INT NOT NULL REFERENCES source_table(id),
    creation_ts TIMESTAMPTZ NOT NULL,
    start_ts TIMESTAMPTZ NOT NULL,
    end_ts TIMESTAMPTZ NOT NULL,
    value FLOAT NOT NULL,
    CONSTRAINT unique_fact UNIQUE (user_id, activity_type_id, unit_id, source_id, creation_ts)
);

-- Create the summary_table with appropriate unique constraints
-- (Add unique constraints as needed based on your CSV extract structure)
CREATE TABLE summary_table (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES user_table(id),
    creation_date DATE NOT NULL,
    active_energy_burned FLOAT,
    active_energy_burned_goal FLOAT,
    active_energy_burned_unit_id INT REFERENCES unit_table(id),
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


