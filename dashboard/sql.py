GET_SUMMARY = """
SELECT creation_date as date, active_energy_burned, exercise_minutes, stand_hours
FROM summary
JOIN users ON summary.user_id = users.id
WHERE users.username = %s
AND creation_date >= %s AND creation_date <= %s
"""