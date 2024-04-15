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
JOIN (SELECT facts.creation_ts::date as wake_up_date, SUM(facts.value / 60) as hours_slept
    FROM facts
        JOIN sources ON facts.source_id = sources.id
        JOIN activity_types ON activity_types.id = facts.activity_type_id
        JOIN users ON facts.user_id = users.id
    WHERE ((activity_type_id = 6) OR (activity_type_id = 17) OR (activity_type_id = 18) OR (activity_type_id = 54)) 
    AND ((EXTRACT(HOUR FROM facts.start_ts) > 17) OR (EXTRACT(HOUR FROM facts.start_ts) < 12)) 
    AND sources.source_name = 'Pillow'
    AND users.username = %s
    GROUP BY facts.creation_ts::date) AS sleep
ON summary.creation_date = sleep.wake_up_date
WHERE users.username = %s AND creation_date >= %s AND creation_date <= %s
ORDER BY summary.creation_date
"""