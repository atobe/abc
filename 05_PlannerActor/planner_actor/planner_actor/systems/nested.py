from typing import Type
from raal.model import Context
from ..agents.react import ReActAgent
from ..agents.planner import PlannerAgent
import sys


class Runner:
    def __init__(self, prompt: str):
        self.context = Context()
        self.context.runner = self
        self.agent_stack = []
        self.count = 0
        self.gosub_agent(PlannerAgent, prompt)
        print('nested runner')

    @property
    def done(self):
        return self.agent_stack == []

    def _show_agent_stack(self):
        for i, agent in enumerate(self.agent_stack[::-1]):
            suffix = ' <<<' if i == 0 else ''
            print(f'{agent}{suffix}')

    def run(self):
        while not self.done:
            self._show_agent_stack()
            agent_done = self.agent_stack[-1].step(indent=len(self.agent_stack) - 1)
            if agent_done:
                self.return_agent(self.agent_stack[-1].final_answer())
            print()
        return self.agent.final_answer()

    def assign_subtask_to_worker(self, task_description):
        # called by the AssignSubtaskToWorker tool
        self.gosub_agent(ReActAgent, task_description)

    def gosub_agent(self, agent_class: Type, task_packet):
        self.count += 1
        self.agent = agent_class(prompt=task_packet, context=self.context)
        self.agent_stack.append(self.agent)
        self.context.agent = self.agent
        # if self.count > 1:
        #     # print the traceback to console
        #     import traceback
        #     traceback.print_stack(file=sys.stdout)
        #     sys.exit()

    def return_agent(self, result: str):
        self.agent_stack.pop()

        # restore the previous agent
        if len(self.agent_stack) > 0:
            self.agent = self.agent_stack[-1]
            self.context.agent = self.agent

            # hand back the result
            self.agent.add_observation(f'Worker finished with: {result}')


def main():
    # prompt = "What is SZA's age squared?"
    prompt = "What is SZAs age squared? Make a plan and then execute it."
    runner = Runner(prompt)
    answer = runner.run()
    print(answer)


if __name__ == "__main__":
    main()
