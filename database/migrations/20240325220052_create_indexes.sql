-- Add migration script here
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_activity_types_activity_name ON activity_types(activity_name);
CREATE INDEX idx_units_unit_name ON units(unit_name);
CREATE INDEX idx_sources_source_name ON sources(source_name);