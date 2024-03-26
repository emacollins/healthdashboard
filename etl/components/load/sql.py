CREATE_TEMP_FACT_TABLE = """
CREATE TEMP TABLE fact_table_temp (
    username TEXT,
    email TEXT,
    activity_category TEXT,
    activity_type_name TEXT,
    unit_name TEXT,
    source_name TEXT,
    creation_ts TIMESTAMPTZ,
    start_ts TIMESTAMPTZ,
    end_ts TIMESTAMPTZ,
    value NUMERIC,
    device_name TEXT,
    device_manufacturer TEXT,
    device_model TEXT,
    device_hardware TEXT,
    device_software TEXT
);
"""

CREATE_SUMMARY_TABLE_FACT = """
CREATE TEMP TABLE summary_table_temp (
    creation_date DATE,
    active_energy_burned FLOAT,
    active_energy_burned_goal FLOAT,
    active_energy_burned_unit TEXT,
    move_time FLOAT,
    move_time_goal FLOAT,
    exercise_minutes FLOAT,
    exercise_minutes_goal FLOAT,
    stand_hours FLOAT,
    stand_hours_goal FLOAT,
    username TEXT
);

"""


COPY_FACT_TABLE = """
COPY fact_table_temp
FROM STDIN WITH (FORMAT csv, HEADER false, DELIMITER ',')
"""

COPY_SUMMARY_TABLE = """
COPY summary_table_temp
FROM STDIN WITH (FORMAT csv, HEADER false, DELIMITER ',')
"""


INSERT_ACTIVITY_TYPES = """
INSERT INTO activity_types (activity_name, category)
    SELECT DISTINCT activity_type_name, activity_category
    FROM fact_table_temp
    ON CONFLICT DO NOTHING
"""

INSERT_UNITS = """
INSERT INTO units (unit_name)
    SELECT DISTINCT unit_name
    FROM fact_table_temp
    ON CONFLICT DO NOTHING
"""

INSERT_SOURCES = """
INSERT INTO sources (source_name, device_name, device_manufacturer, device_model, device_hardware, device_software)
    SELECT DISTINCT source_name, device_name, device_manufacturer, device_model, device_hardware, device_software
    FROM fact_table_temp
    ON CONFLICT DO NOTHING
"""

INSERT_USERS = """
INSERT INTO users (username, email)
    SELECT DISTINCT username, email
    FROM fact_table_temp
    ON CONFLICT DO NOTHING
"""


INSERT_FACT_TABLE = """
INSERT INTO facts (user_id, activity_type_id, unit_id, source_id, creation_ts, start_ts, end_ts, value)
    SELECT users.id, activity_types.id, units.id, s.id, f.creation_ts, f.start_ts, f.end_ts, f.value
        FROM (fact_table_temp f
        JOIN users ON f.username = users.username
        JOIN activity_types ON f.activity_type_name = activity_types.activity_name
        JOIN units ON f.unit_name = units.unit_name
        JOIN sources s ON (f.source_name, f.device_name, f.device_manufacturer, f.device_model, f.device_hardware, f.device_software) = (s.source_name, s.device_name, s.device_manufacturer, s.device_model, s.device_hardware, s.device_software))
ON CONFLICT DO NOTHING
"""

INSERT_SUMMARY_TABLE = """
INSERT INTO summary (user_id, creation_date, active_energy_burned, active_energy_burned_goal, active_energy_burned_unit_id, move_time, move_time_goal, exercise_minutes, exercise_minutes_goal, stand_hours, stand_hours_goal)
    SELECT users.id, s.creation_date, s.active_energy_burned, s.active_energy_burned_goal, units.id, s.move_time, s.move_time_goal, s.exercise_minutes, s.exercise_minutes_goal, s.stand_hours, s.stand_hours_goal
        FROM (summary_table_temp s
        JOIN users on s.username = users.username
        JOIN units on s.active_energy_burned_unit = units.unit_name
        )
ON CONFLICT DO NOTHING
"""
