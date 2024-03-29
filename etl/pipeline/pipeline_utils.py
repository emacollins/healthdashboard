import time
import boto3


class ECSTask:
    def __init__(
        self,
        cluster_name: str,
        task_definition: str,
        task_args: list,
        region_name: str,
        launch_type: str,
        max_run_time: int,
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

        Attributes:
            poll_time (int): The interval in seconds between task status checks.
            elapsed_run_time (int): The elapsed run time of the task in seconds.
            task_args (list): The arguments to pass to the task.
            cluster_name (str): The name of the ECS cluster.
            task_definition (str): The ARN of the task definition.
            launch_type (str): The launch type for the task.
            max_run_time (int): The maximum run time for the task in seconds.
            ecs_client (boto3.client): The ECS client.

        """
        self.poll_time = 10  # in units of seconds
        self.elapsed_run_time = 0

        self.task_args = task_args
        self.cluster_name = cluster_name
        self.task_definition = task_definition
        self.launch_type = launch_type
        self.max_run_time = max_run_time
        self.ecs_client = boto3.client("ecs", region_name=region_name)

    def run(self):
        """Given task definition, runs the ECS task and waits for it to complete."""
        response = self.ecs_client.run_task(
            cluster=self.cluster_name,
            launchType=self.launch_type,  # or 'EC2' depending on your configuration
            taskDefinition=self.task_definition,
            count=1,
        )

        # Extract the task ARN
        self.task_arn = response["tasks"][0]["taskArn"]
        complete, stopped_reason = self._check_if_complete()
        return complete, stopped_reason

    def _check_if_complete(self):
        """Check if the ECS task has completed."""

        while True:
            if self.elapsed_run_time > self.max_run_time:
                reason = "Task timed out"
                self._stop_ecs_task(reason=reason)
                return False, reason
            # Check the task status
            response = self.ecs_client.describe_tasks(
                cluster=self.cluster_name, tasks=[self.task_arn]
            )
            task_status = response["tasks"][0]["lastStatus"]
            if task_status == "STOPPED":
                stopped_reason = response["tasks"][0]["stoppedReason"]
                return True, stopped_reason

            time.sleep(self.poll_time)  # Poll every 10 seconds. Adjust as necessary.
            self.elapsed_time = self.elapsed_run_time + self.poll_time

    def _stop_ecs_task(self, reason):
        response = self.ecs_client.stop_task(
            cluster=self.cluster_name, task=self.task_arn, reason=reason
        )
        return response
