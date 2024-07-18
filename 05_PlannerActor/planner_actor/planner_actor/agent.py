from typing import Optional
from raal.agent import (
    init_agent,
    step_agent,
    is_done,
    extract_final_answer,
    add_observation,
)
from raal.agentlib import show_chunks_compact
from raal.model import Context


class Agent:
    UPDATES_SYSTEM_PROMPT = False
    count = 1

    def __init__(self, prompt: str, context: Context):
        self.name = f'Agent-{self.__class__.__name__}-{self.count}'
        self.count += 1
        self.tools = self.get_tools()
        self.state = init_agent(
            prompt=prompt,
            tools=self.tools,
            context=context,
            system_prompt=(
                self.get_system_prompt() if not self.UPDATES_SYSTEM_PROMPT else None
            ),
        )

    def get_system_prompt(self):
        return None

    def step(self, indent=0):
        if is_done(self.state):
            return True

        # if self.UPDATES_SYSTEM_PROMPT:
        #     self.state.system_prompt = self.get_system_prompt()

        self.state = step_agent(self.state)
        indent = '    '*indent
        color = 'green' if 'Planner' in self.__class__.__name__ else 'magenta'
        show_chunks_compact(self.state, prefix=f'{indent}{self.__class__.__name__}:', color=color)
        return is_done(self.state)

    def add_observation(self, text: Optional[str] = None):
        if text:
            add_observation(self.state, text)

    def run(self):
        while not self.step():
            pass
        return extract_final_answer(self.state)

    def is_done(self):
        return is_done(self.state)

    def final_answer(self):
        return extract_final_answer(self.state)
    
    def __repr__(self):
        return self.name
