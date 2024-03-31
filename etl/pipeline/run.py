import boto3
import time
import os

import pipeline_utils as utils
import pipeline_config as config
from dotenv import load_dotenv

# Load .env file if it exists
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def main():
    # Define your tasks in the order they need to be executed

    EXTRACT_TASK = utils.ECSTask(
        cluster_name=config.TASK_CONFIG["EXTRACT"]["cluster_name"],
        task_definition=config.TASK_CONFIG["EXTRACT"]["task_definition"],
        task_args=[],
        region_name=config.TASK_CONFIG["EXTRACT"]["region_name"],
        launch_type=config.TASK_CONFIG["EXTRACT"]["launch_type"],
        max_run_time=config.TASK_CONFIG["EXTRACT"]["max_run_time"],
    )

    TRANSFORM_TASK = utils.ECSTask(
        cluster_name=config.TASK_CONFIG["TRANSFORM"]["cluster_name"],
        task_definition=config.TASK_CONFIG["TRANSFORM"]["task_definition"],
        task_args=[],
        region_name=config.TASK_CONFIG["TRANSFORM"]["region_name"],
        launch_type=config.TASK_CONFIG["TRANSFORM"]["launch_type"],
        max_run_time=config.TASK_CONFIG["TRANSFORM"]["max_run_time"],
    )

    LOAD_TASK = utils.ECSTask(
        cluster_name=config.TASK_CONFIG["LOAD"]["cluster_name"],
        task_definition=config.TASK_CONFIG["LOAD"]["task_definition"],
        task_args=[],
        region_name=config.TASK_CONFIG["LOAD"]["region_name"],
        launch_type=config.TASK_CONFIG["LOAD"]["launch_type"],
        max_run_time=config.TASK_CONFIG["LOAD"]["max_run_time"],
    )
    
    EXTRACT_TASK.run()
    time.sleep(10)
    TRANSFORM_TASK.run()
    time.sleep(10)
    LOAD_TASK.run()


if __name__ == "__main__":
    main()
