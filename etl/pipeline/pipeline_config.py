import os
from dotenv import load_dotenv

# Load .env file if it exists
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TASK_CONFIG = {
    "EXTRACT": {
        "cluster_name": os.environ["CLUSTER_NAME"],
        "task_definition": os.environ["EXTRACT_TASK_DEFINITION"],
        "region_name": os.environ["REGION_NAME"],
        "launch_type": os.environ["LAUNCH_TYPE"],
        "max_run_time": 300 # seconds
    },
    "TRANSFORM": {
        "cluster_name": os.environ["CLUSTER_NAME"],
        "task_definition": os.environ["TRANSFORM_TASK_DEFINITION"],
        "region_name":  os.environ["REGION_NAME"],
        "launch_type": os.environ["LAUNCH_TYPE"],
        "max_run_time": 300 # seconds
    },
    "LOAD": {
        "cluster_name": os.environ["CLUSTER_NAME"],
        "task_definition": os.environ["LOAD_TASK_DEFINITION"],
        "region_name": os.environ["REGION_NAME"],
        "launch_type": os.environ["LAUNCH_TYPE"],
        "max_run_time": 600 # seconds
    }
}
