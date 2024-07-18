from typing import Type
from raal.model import Context
from ..agents.react import ReActAgent
from ..agents.planner import PlannerAgent


class Runner:
    def __init__(self, prompt: str):
        self.context = Context()
        self.context.runner = self
        self.agent = ReActAgent(prompt=prompt, context=self.context)
        self.context.agent = self.agent

    def run(self):
        while not self.agent.step():
            pass
        return self.agent.final_answer()
