import psycopg2
import pandas as pd
import os

import logging

import constants

from typing import Dict, Tuple, List


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

class DataLoader():
    def __init__(self, fact_tables: Dict[str, pd.DataFrame], environment: str):
        """Used to load data into the database"""
        self.fact_tables = fact_tables
        self.environment = environment

        

    def load(self):
        logger.info("Starting load")
        for table_name, table in self.fact_tables.items():
            if type(table) != pd.DataFrame:
                logger.warning(f"Table {table_name} is not a DataFrame")
                continue
            if table_name == "fact_table":
                # Code to load table1
                pass
            elif table_name == "summary_table":
                # Code to load table2
                pass
            else:
                logger.warning(f"Unknown table: {table_name}")

    def _load_fact_table(self, table: pd.DataFrame) -> None:
        with psycopg2.connect(
            dbname=constants.DATABASE_CONFIG[self.environment]["dbname"],
            user=constants.DATABASE_CONFIG[self.environment]["user"],
            password=constants.DATABASE_CONFIG[self.environment]["password"],
            host=constants.DATABASE_CONFIG[self.environment]["host"],
            port=constants.DATABASE_CONFIG[self.environment]["port"],
        ) as conn:
            # TODO: Load the fact table
            pass