import pandas as pd
import constants
import argparse
import boto3

from typing import Dict

import logging
import re

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Add formatter to handler
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)



def get_fact_table_files(fact_table_directory: str) -> Dict[str, pd.DataFrame]:
    """Get the list of fact table files from the directory"""

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



def main(fact_table_directory: str, environment: str) -> None:
    """Load service inserts data into the database"""
    if environment not in constants.DATABASE_CONFIG.keys():
        logger.error(f"Unknown environment: {environment}")
        assert 1 == 0
    
    logger.info(f"Starting Load Process: {fact_table_directory}")

    fact_tables = get_fact_table_files(fact_table_directory)

    
    

    logger.info("Load Process Complete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Health Dashboard Transform Process")
    parser.add_argument(
        "--fact_table_directory",
        type=str,
        help="Path to the directory containing the fact tables Can be local directory or S3 URI",
    )
    parser.add_argument(
        "--environement",
        type=str,
        help="Environment to run the process in. DEV or PROD",
    )
    args = parser.parse_args()
    main(args.fact_table_director, args.environment)
