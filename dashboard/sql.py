GET_SUMMARY_OLD = """
SELECT creation_date as date, active_energy_burned, exercise_minutes
FROM summary
JOIN users ON summary.user_id = users.id
WHERE users.username = %s
AND creation_date >= %s AND creation_date <= %s
"""

# Second join queries sleep data from facts table.
# Activity_type_id 10 corresponds to "InBed" activity.
# Sleep data is filtered to include only data from 6 PM to 5 AM.
GET_SUMMARY = """
SELECT summary.creation_date as date, summary.active_energy_burned, summary.exercise_minutes, sleep.hours_slept
FROM summary
JOIN users ON summary.user_id = users.id
JOIN (SELECT f.start_ts::date as sleep_date, f.end_ts::date as wake_up_date, f.value / 60 as hours_slept
            FROM facts f
            JOIN activity_types ON activity_types.id = f.activity_type_id
			JOIN users ON users.id = f.user_id
            WHERE (activity_type_id = 10) 
				AND ((EXTRACT(HOUR FROM f.start_ts) > 17) 
				OR (EXTRACT(HOUR FROM f.start_ts) < 5))
				AND users.username = %s) AS sleep
ON summary.creation_date = sleep.sleep_date
WHERE users.username = %s AND creation_date >= %s AND creation_date <= %s
ORDER BY summary.creation_date
"""