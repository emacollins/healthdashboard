FACT_TABLE_FILENAME = "fact_table.csv.gz"
SUMMARY_TABLE_FILENAME = "summary_table.csv.gz"

summary_column_rename_map = {
    "dateComponents": "creation_date",
    "activeEnergyBurned": "active_energy_burned",
    "activeEnergyBurnedGoal": "active_energy_burned_goal",
    "activeEnergyBurnedUnit": "active_energy_burned_unit",
    "appleMoveTime": "move_time",
    "appleMoveTimeGoal": "move_time_goal",
    "appleExerciseTime": "exercise_minutes",
    "appleExerciseTimeGoal": "exercise_minutes_goal",
    "appleStandHours": "stand_hours",
    "appleStandHoursGoal": "stand_hours_goal",
}

workout_column_rename_map = {
    "workoutActivityType": "type",
    "duration": "value",
    "durationUnit": "unit",
}

fact_table_column_rename_map = {
    "type": "activity_type_name",
    "unit": "unit_name",
    "sourceName": "source_name",
    "creationDate": "creation_ts",
    "startDate": "start_ts",
    "endDate": "end_ts",
    "value": "value",
    "name": "device_name",
    "manufacturer": "device_manufacturer",
    "model": "device_model",
    "hardware": "device_hardware",
    "software": "device_software",
}

type_prefixes = {
    "HKCategoryTypeIdentifier": "category",
    "HKQuantityTypeIdentifier": "quantity",
    "HKWorkoutActivityType": "workout",
    "HKCategoryValueSleepAnalysis": "sleep",
}

activity_types_to_drop = ["LowHeartRateEvent", "HeadphoneAudioExposureEvent"]

fact_table_final_columns = [
    "username",
    "email",
    "activity_category",
    "activity_type_name",
    "unit_name",
    "source_name",
    "creation_ts",
    "start_ts",
    "end_ts",
    "value",
    "device_name",
    "device_manufacturer",
    "device_model",
    "device_hardware",
    "device_software",
]
