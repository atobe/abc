from ..model import Tool, Observation


class RevisePlan(Tool):
    """Revise the plan for a project."""

    def __call__(self, lines_of_plan: str):
        lines = lines_of_plan.split("\n")
        self.context.agent.state.plan = lines_of_plan
        return Observation(f"Plan revised. {len(lines)} steps.")
