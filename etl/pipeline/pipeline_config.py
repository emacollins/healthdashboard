import os

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
}
