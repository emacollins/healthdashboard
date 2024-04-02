import os
from dotenv import load_dotenv

# Load .env file if it exists
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# TODO: Dynamic user based on the user that triggered the pipeline
TASK_CONFIG = {
    "EXTRACT": {
        "args": {"--input_path": "s3://applehealthdashboard/etl/harvest/export.zip"},
        "cluster_name": os.environ["CLUSTER_NAME"],
        "task_definition": os.environ["EXTRACT_TASK_DEFINITION"],
        "container_name": os.environ["EXTRACT_CONTAINER_NAME"],
        "region_name": os.environ["REGION_NAME"],
        "launch_type": os.environ["LAUNCH_TYPE"],
        "max_run_time": 300 # seconds
    },
    "TRANSFORM": {
        "args": {"--record_input_path": "s3://applehealthdashboard/etl/extract/exportRecord.csv.gz",
                 "--workout_input_path": "s3://applehealthdashboard/etl/extract/exportWorkout.csv.gz",
                 "--summary_input_path": "s3://applehealthdashboard/etl/extract/exportActivitySummary.csv.gz",
                 "--output_directory": "s3://applehealthdashboard/etl/transform/",
                 "--username": "eric",
                 "--email": "test@test.com"},
        "cluster_name": os.environ["CLUSTER_NAME"],
        "task_definition": os.environ["TRANSFORM_TASK_DEFINITION"],
        "container_name": os.environ["TRANSFORM_CONTAINER_NAME"],
        "region_name":  os.environ["REGION_NAME"],
        "launch_type": os.environ["LAUNCH_TYPE"],
        "max_run_time": 300 # seconds
    },
    "LOAD": {
        "args": {"--fact_table_directory": "s3://applehealthdashboard/etl/transform/",
                 "--environment": "DEV"},
        "cluster_name": os.environ["CLUSTER_NAME"],
        "task_definition": os.environ["LOAD_TASK_DEFINITION"],
        "container_name": os.environ["LOAD_CONTAINER_NAME"],
        "region_name": os.environ["REGION_NAME"],
        "launch_type": os.environ["LAUNCH_TYPE"],
        "max_run_time": 600 # seconds
    }
}
