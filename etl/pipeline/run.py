import boto3
import time
import os

import pipeline_utils as utils
import pipeline_config as config

import logging

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


def create_task(task_config):
    return utils.ECSTask(
        cluster_name=task_config["cluster_name"],
        task_definition=task_config["task_definition"],
        task_args=[],
        region_name=task_config["region_name"],
        launch_type=task_config["launch_type"],
        max_run_time=task_config["max_run_time"],
    )


def main():
    # Define your tasks in the order they need to be executed
    tasks = ["EXTRACT", "TRANSFORM", "LOAD"]
    task_objects = {task: create_task(config.TASK_CONFIG[task]) for task in tasks}

    for task in tasks:
        logger.info(f"Running task: {task}")
        complete, response = task_objects[task].run()
        if complete:
            logger.info(f"{task} task completed: {response}")
        else:
            logger.error(f"{task} task failed to complete: {response}")


if __name__ == "__main__":
    main()
