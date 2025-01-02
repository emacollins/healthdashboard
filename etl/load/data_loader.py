import psycopg2
import pandas as pd
import io
import logging

import etl.load.constants as constants
import etl.load.sql as sql

from typing import Dict


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

            # Tables should always be passed in as pandas dataframes
            if type(table) != pd.DataFrame:
                logger.warning(f"Table {table_name} is not a DataFrame")
                continue
                
            # If more fact tables are added, add addtional if statement and loader function
            if table_name == "fact_table":
                self._load_fact_table(table=table)
                logger.info(f"{table_name} loaded")
            elif table_name == "summary_table":
                self._load_summary_table(table=table)
                logger.info(f"{table_name} loaded")
            else:
                logger.warning(f"Unknown table: {table_name}")
    
    def _load_summary_table(self, table: pd.DataFrame) -> None:
        with psycopg2.connect(
            dbname=constants.DATABASE_CONFIG[self.environment]["dbname"],
            user=constants.DATABASE_CONFIG[self.environment]["user"],
            password=constants.DATABASE_CONFIG[self.environment]["password"],
            host=constants.DATABASE_CONFIG[self.environment]["host"],
            port=constants.DATABASE_CONFIG[self.environment]["port"],
        ) as conn:
            
            cur = conn.cursor()

            # Create a temporary table
            cur.execute(sql.CREATE_SUMMARY_TABLE_FACT)

            # Copy the data from the StringIO object into the database
            cur.copy_expert(sql.COPY_SUMMARY_TABLE, self._read_df_into_memory(table))

            cur.execute(sql.INSERT_SUMMARY_TABLE)
        
        



    def _load_fact_table(self, table: pd.DataFrame) -> None:
        with psycopg2.connect(
            dbname=constants.DATABASE_CONFIG[self.environment]["dbname"],
            user=constants.DATABASE_CONFIG[self.environment]["user"],
            password=constants.DATABASE_CONFIG[self.environment]["password"],
            host=constants.DATABASE_CONFIG[self.environment]["host"],
            port=constants.DATABASE_CONFIG[self.environment]["port"],
        ) as conn:
            
            cur = conn.cursor()

            # Create a temporary table
            cur.execute(sql.CREATE_TEMP_FACT_TABLE)

            # Copy the data from the StringIO object into the database
            cur.copy_expert(sql.COPY_FACT_TABLE, self._read_df_into_memory(table))

            cur.execute(sql.INSERT_ACTIVITY_TYPES)
            cur.execute(sql.INSERT_UNITS)
            cur.execute(sql.INSERT_SOURCES)
            cur.execute(sql.INSERT_USERS)
            cur.execute(sql.INSERT_FACT_TABLE)


    def _read_df_into_memory(self, table: pd.DataFrame) -> object:
        sio = io.StringIO()
        sio.write(table.to_csv(index=False, header=False))
        sio.seek(0)
        return sio