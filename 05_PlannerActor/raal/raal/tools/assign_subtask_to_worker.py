from ..model import Tool, Observation


class AssignSubtaskToWorker(Tool):
    """Give a task to another agent to complete. You will be notified when it is done."""

    def __call__(self, task_description: str):
        self.context.runner.assign_subtask_to_worker(task_description)
        # return None because Observation will be added when the worker finishes
        return None
