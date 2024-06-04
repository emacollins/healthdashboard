GET_SUMMARY = """
SELECT summary.creation_date as date, calories.total_calories, summary.exercise_minutes, sleep.hours_slept
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
    GROUP BY facts.creation_ts::date
    ) AS sleep
ON summary.creation_date = sleep.wake_up_date
JOIN (SELECT facts.creation_ts::date as creation_date, SUM(facts.value) as total_calories
    FROM facts
        JOIN sources ON facts.source_id = sources.id
        JOIN users ON facts.user_id = users.id
    WHERE (activity_type_id = 53 OR activity_type_id = 40) AND users.username = %s
    GROUP BY facts.creation_ts::date
    ) AS calories
ON summary.creation_date = calories.creation_date
WHERE users.username = %s AND summary.creation_date >= %s AND summary.creation_date <= %s
ORDER BY summary.creation_date
"""

GET_TOTAL_CALORIES = """
SELECT SUM(value) as cals
FROM facts
JOIN users ON facts.user_id = users.id
WHERE (activity_type_id = 53 OR activity_type_id = 40) 
AND users.username = %s 
AND facts.creation_ts::date >= %s AND facts.creation_ts::date <= %s
"""

GET_TOTAL_EXERCISE_MINUTES = """
SELECT SUM(summary.exercise_minutes) as total_mins
FROM summary
JOIN users ON summary.user_id = users.id
AND users.username = %s 
AND summary.creation_date >= %s AND summary.creation_date <= %s
"""

GET_EXERCISE_COUNT = """
SELECT COUNT(f.creation_ts::date), a.activity_name
FROM facts f
JOIN activity_types a ON a.id = f.activity_type_id
JOIN users ON f.user_id = users.id
WHERE a.category = 'workout' 
AND users.username = %s 
AND f.creation_ts >= %s 
AND f.creation_ts <= %s
GROUP BY a.activity_name
"""