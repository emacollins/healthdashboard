# Health Dashboard Load Process
This Python script is used to load data into a database for a health dashboard. The data is loaded from fact tables, which can be located either in a local directory or in an Amazon S3 bucket.

## Dependencies
* pandas
* boto3
* psycopg2

## How to Run
The script is run from the command line with two arguments:

* `--fact_table_directory`: The path to the directory containing the fact tables. This can be a local directory or an S3 URI.
* `--environment`: The environment to run the process in. This can be either DEV or LOCAL.

## Example usage:

```bash
python run.py --fact_table_directory /path/to/fact/tables --environment DEV
```

## Functionality
The script first checks if the provided environment is valid. If not, it logs an error and stops execution.

Next, it determines whether the fact table directory is a local directory or an S3 URI. If it's an S3 URI, it parses the URI into a bucket and key, and retrieves the list of file paths from the S3 bucket. If it's a local directory, it generates the list of file paths based on the names of the fact tables.

The script then loads the fact tables into pandas DataFrames, and logs the names of the tables to be loaded.

Finally, it creates a DataLoader object with the fact tables and the environment, and calls the load method to load the data into the database.

## Build

`docker build -t healthdashboard/etl/load`

The `build.sh` script will automate building and pushing the image to your AWS ECR repo.