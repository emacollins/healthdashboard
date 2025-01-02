-- Some records had the same creation_ts but were unique data, so update to use start_ts and end_ts as unique constraints
BEGIN;
ALTER TABLE facts DROP CONSTRAINT IF EXISTS unique_fact;
ALTER TABLE facts ADD CONSTRAINT unique_fact UNIQUE (user_id, activity_type_id, unit_id, source_id, start_ts, end_ts, value);
COMMIT;