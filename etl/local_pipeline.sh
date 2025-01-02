#!/bin/bash

# Extract
docker run -v "$(pwd)/data:/data" extract --input_path /data/etl/harvest/export.zip &&

#transform
docker run -v "$(pwd)/data:/data" transform --record_input_path /data/etl/extract/exportRecord.csv.gz --workout_input_path /data/etl/extract/exportWorkout.csv.gz --summary_input_path /data/etl/extract/exportActivitySummary.csv.gz --output_directory /data/etl/transform --username eric --email test@test.com &&

#load
docker run -v "$(pwd)/data:/data" load --fact_table_directory /data/etl/transform --environment LOCAL