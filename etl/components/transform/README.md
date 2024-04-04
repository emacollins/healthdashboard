# Health Data Transform Process

This Python script is used to transform health data for a health dashboard. The data is loaded from CSV files, which can be located either in a local directory or in an Amazon S3 bucket.

## Dependencies

- pandas
- boto3
- argparse
- re
- logging
- constants (a local module)

## How to Run

The script is run from the command line with the following arguments:

1. `--record_input_path`: The path to the "exportRecord" CSV file. This can be a local directory or an S3 URI.
2. `--workout_input_path`: The path to the "exportWorkout" CSV file. This can be a local directory or an S3 URI.
3. `--summary_input_path`: The path to the "exportActivitySummary" CSV file. This can be a local directory or an S3 URI.
4. `--output_directory`: The output directory path. This can be a local directory or an S3 URI.
5. `--username`: The username of the data owner.
6. `--email`: The email of the data owner.

Example usage:

```bash
python run.py --record_input_path /path/to/exportRecord.csv --workout_input_path /path/to/exportWorkout.csv --summary_input_path /path/to/exportActivitySummary.csv --output_directory /path/to/output --username user --email user@example.com
```

## Functionality

The script first loads the data from the specified input paths. If the paths are S3 URIs, it uses the boto3 library to retrieve the data from the S3 bucket. If the paths are local directories, it reads the data directly from the CSV files.

Next, it processes the sleep data in the record data frame, converting the categorical sleep data into a quantifiable duration of sleep.

Then, it transforms and cleans the final fact table, which includes unpacking key-value pairs in the 'device' column, renaming columns to match database table column names, cleaning up the activity_type_name, and filtering out records that are not useful.

The script also processes the summary data separately, as it involves a different process.

Finally, it saves the transformed data to the specified output directory. If the directory is an S3 URI, it uploads the data to the S3 bucket. If the directory is a local directory, it saves the data directly to the CSV files.

## Logging

The script uses Python's built-in logging module to log information and errors. The log messages are formatted with the time, the name of the logger, the log level, and the message, and are output to the console.