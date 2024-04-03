import boto3
import os

ssm = boto3.client("ssm")

FACT_TABLES = ["fact_table", "summary_table"]
DATABASE_CONFIG = {
    "LOCAL": {
        "dbname": "applehealth",
        "user": "ericcollins",
        "password": os.environ.get("DB_PASSWORD"),
        "host": "host.docker.internal",
        "port": "5432",
    },
    "DEV": {
        "dbname": "applehealth",
        "user": "eric",
        "password": ssm.get_parameter(
            Name="APPLEHEALTH_DEV_DB_PW", WithDecryption=True
        )["Parameter"]["Value"],
        "host": ssm.get_parameter(Name="APPLEHEALTH_DEV_DB_HOST", WithDecryption=True)[
            "Parameter"
        ]["Value"],
        "port": "5432",
    },
}
