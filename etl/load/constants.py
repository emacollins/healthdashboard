import os

FACT_TABLES = ["fact_table", "summary_table"]
DATABASE_CONFIG = {
    "LOCAL": {
        "dbname": "applehealth",
        "user": "ericcollins",
        "password": os.environ.get("DB_PASSWORD"),
        "host": "host.docker.internal",
        "port": "5432",
    },
}
