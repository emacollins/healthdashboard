import pandas as pd
import constants
import argparse
import boto3

from typing import Dict, Tuple, List

import logging
import re

from data_loader import DataLoader

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter("Load - %(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Add formatter to handler
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)



def get_fact_table_files(fact_table_directory: str) -> Dict[str, pd.DataFrame]:
    """Get the list of fact table files from the directory"""

    if fact_table_directory.startswith("s3://"):
        # Handle S3 URI
        s3_bucket, s3_key = parse_s3_directory_uri(fact_table_directory)
        fact_table_files = get_s3_file_uris(s3_bucket, s3_key)
    else:
        # Handle local directory
        if fact_table_directory[-1] == "/":
            fact_table_directory = fact_table_directory[:-1]
        fact_table_files = [
            f"{fact_table_directory}/{table_name}.csv.gz"
            for table_name in constants.FACT_TABLES
        ]

    # Load the fact tables
    fact_tables = {
        table_name: pd.read_csv(file_path, compression="gzip")
        for table_name, file_path in zip(constants.FACT_TABLES, fact_table_files)
    }

    return fact_tables


def parse_s3_directory_uri(s3_uri: str) -> Tuple[str, str]:
    """Parse S3 URI into bucket and key"""
    s3_uri = s3_uri[5:]  # Remove "s3://" prefix
    s3_parts = s3_uri.split("/")
    s3_bucket = s3_parts[0]
    s3_key = "/".join(s3_parts[1:])
    return s3_bucket, s3_key


def get_s3_file_uris(s3_bucket: str, s3_key: str) -> List[str]:
    """Get the list of file paths from S3 bucket and key"""
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_key)
    file_paths = [f"s3://{s3_bucket}/{obj['Key']}" for obj in response["Contents"]]
    return file_paths



def main(fact_table_directory: str, environment: str) -> None:
    """Load service inserts data into the database"""

    if environment not in constants.DATABASE_CONFIG.keys():
        logger.error(f"Unknown environment: {environment}")
        assert 1 == 0

    logger.info(f"Starting Load Service...")

    #All fact tables and their names in format: {table_name: pd.DataFrame, ...}
    fact_tables = get_fact_table_files(fact_table_directory)
    logger.info(f"Fact Tables to be loaded: {', '.join(fact_tables.keys())}")

    loader = DataLoader(fact_tables, environment)
    loader.load()
    
    logger.info("Load Process Complete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Health Dashboard Transform Process")
    parser.add_argument(
        "--fact_table_directory",
        type=str,
        help="Path to the directory containing the fact tables Can be local directory or S3 URI",
    )
    parser.add_argument(
        "--environment",
        type=str,
        help="Environment to run the process in. DEV or PROD",
    )
    args = parser.parse_args()
    main(args.fact_table_directory, args.environment)
