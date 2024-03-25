CREATE_TEMP_FACT_TABLE = """
CREATE TEMP TABLE fact_table_temp (
    username TEXT,
    email TEXT,
    activity_category TEXT,
    activity_type_name TEXT,
    unit_name TEXT,
    source_name TEXT,
    creation_ts TEXT,
    start_ts TEXT,
    end_ts TEXT,
    value NUMERIC,
    device_name TEXT,
    device_manufacturer TEXT,
    device_model TEXT,
    device_hardware TEXT,
    device_software TEXT
);
"""

INSERT_ACTIVITY_TYPES = """
INSERT INTO activity_types (activity_name, category)
    SELECT DISTINCT activity_name, activity_category
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
    SELECT users.id, activity_types.id, units.id, sources.id, creation_ts, start_ts, end_ts, value
        FROM (fact_table_temp
        JOIN users ON fact_table_temp.username = users.username
        JOIN activity_types ON fact_table_temp.activity_type_name = activity_types.activity_name
        JOIN units ON fact_table_temp.unit_name = units.unit_name
        JOIN sources ON fact_table_temp.source_name = sources.source_name)
    ON CONFLICT DO NOTHING
"""
