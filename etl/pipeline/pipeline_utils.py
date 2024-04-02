import time
import boto3
import botocore.exceptions
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


class ECSTask:
    def __init__(
        self,
        cluster_name: str,
        task_definition: str,
        container_name: str,
        task_args: list,
        region_name: str,
        launch_type: str,
        max_run_time: int,
        poll_time: int = 10,
    ):
        """
        A utility class for running and monitoring ECS tasks.

        Args:
            cluster_name (str): The name of the ECS cluster.
            task_definition (str): The ARN of the task definition.
            task_args (list): A list of arguments to pass to the task.
            region_name (str): The AWS region name.
            launch_type (str): The launch type for the task.
            max_run_time (int): The maximum run time for the task in seconds.
            poll_time (int): The interval in seconds between task status checks.

        Attributes:
            poll_time (int): The interval in seconds between task status checks.
            elapsed_run_time (int): The elapsed run time of the task in seconds.
            task_args (list): The arguments to pass to the task.
            cluster_name (str): The name of the ECS cluster.
            task_definition (str): The ARN of the task definition.
            launch_type (str): The launch type for the task. Generally FARGATE or EC2.
            max_run_time (int): The maximum run time for the task in seconds.
            ecs_client (boto3.client): The ECS client.

        """
        self.poll_time = poll_time  # in units of seconds
        self.elapsed_run_time = 0

        self.container_name = container_name
        self.cluster_name = cluster_name
        self.task_definition = task_definition
        self.launch_type = launch_type
        self.max_run_time = max_run_time

        self.task_args = [f"{key} {value}" for key, value in task_args.items()]

        try:
            self.ecs_client = boto3.client("ecs", region_name=region_name)
        except botocore.exceptions.NoCredentialsError:
            print("No AWS credentials found.")
            raise
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error initializing boto3 ECS client: {e}")
            raise
        
        

    def run(self):
        """Given task definition, runs the ECS task and waits for it to complete."""
        try:
            response = self.ecs_client.run_task(
                cluster=self.cluster_name,
                launchType=self.launch_type,
                taskDefinition=self.task_definition,
                count=1,
                overrides={
                    "containerOverrides": [
                        {"name": self.container_name, "command": self.task_args},
                    ]
                },
            )
        except botocore.exceptions.BotoCoreError as e:
            print(f"Error running task: {e}")
            raise

        # Extract the task ARN
        self.task_arn = response["tasks"][0]["taskArn"]
        complete, stopped_reason = self._check_if_complete()
        return complete, stopped_reason

    def _check_if_complete(self):
        """Check if the ECS task has completed.
        If task status returns STOPPED, return True and the stopped reason.
        If task times out, stop the task and return False and the reason."""

        while True:
            if self.elapsed_run_time > self.max_run_time:
                reason = "Task timed out"
                self._stop_ecs_task(reason=reason)
                return False, reason
            # Check the task status
            try:
                response = self.ecs_client.describe_tasks(
                    cluster=self.cluster_name,
                    tasks=[self.task_arn],
                )
            except botocore.exceptions.BotoCoreError as e:
                print(f"Error describing task: {e}")
                raise

            task_status = response["tasks"][0]["lastStatus"]
            if task_status == "STOPPED":
                stopped_reason = response["tasks"][0]["stoppedReason"]
                return True, stopped_reason

            time.sleep(self.poll_time)  # Poll every 10 seconds. Adjust as necessary.
            self.elapsed_run_time = self.elapsed_run_time + self.poll_time

    def _stop_ecs_task(self, reason):
        """Stop the ECS task with the given reason."""
        self.ecs_client.stop_task(
            cluster=self.cluster_name, task=self.task_arn, reason=reason
        )
