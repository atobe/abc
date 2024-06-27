from devtools import pprint

from lats.apps._base import App
from lats.model import Node, InputNode
from lats.llm import call_llm
from raal.agent import init_agent, step_agent, is_done, extract_messages
from raal.agentlib import get_terminal_width, count_steps
from raal.tools import WikipediaSearch, Calculator
from raal.llm import cache

evaluation_prompt = """
How well did the sequence of steps go?
Do you think it will lead to completion of the task.
Answer in the range 0.0 to 1.0 
0.0 - something is fundamentally wrong, this will not succeed.
0.3 - this is looking pessimistic, likely some other approach is needed.
0.6 - this is looking okay, but there are some issues.
0.8 - this is looking good, it is worth continuing.
1.0 - if the whole task is complete, and answered correctly, this is the right score.
Reply only with the number.
"""

def show_compact(step_name, node):
    width = get_terminal_width()
    s = f'{step_name}: {str(node)}'
    s = s[:width]
    print(s)

class Agent(App):
    REQUIRES_CASE = True

    def __init__(self, prompt=None):
        self.prompt = prompt

    def get_root_node(self) -> Node:
        show_compact('get_root_node', None)
        return InputNode(prompt_or_question=self.prompt)

    def _complete_node(self, node: Node):
        state_ = step_agent(node.state)
        new_node = Node(
            parent=node,
            messages=[],
            observation=None,
            source=None,
            test_feedback=None,
            state=state_,
        )
        # new_node.finished = is_done(state_)
        # new_node.observation = 0.5 if new_node.finished else 0.0
        new_node.observation = 0.1
        new_node.subcount = count_steps(state_)
        return new_node

    def expand_InputNode(self, node: Node) -> Node:
        show_compact('expand_InputNode', node)
        tools = [WikipediaSearch, Calculator]
        node.state = init_agent(node.prompt_or_question, tools)
        return self._complete_node(node)

    def expand_Node(self, node: Node) -> Node:
        show_compact('expand_Node', node)
        return self._complete_node(node)

    def evaluate(self, node: Node) -> float:
        state = node.state
        # if node.finished:
        #     return 1.0
        pre_message = [
            {
                "role": "user",
                "content": "I am replaying this conversation for you. Read the steps closely. I am going to ask you to make a judgment about how well this is going.",
            }
        ]
        messages = extract_messages(state, all_messages=True, trim=1)
        post_message = [
            {
                "role": "user",
                "content": evaluation_prompt,
            }
        ]
        messages = pre_message + messages + post_message
        response = call_llm(messages, temperature=0.0)
        # print('='*80)
        # pprint(messages)
        # print('~'*80)
        # print(response)
        # print('~'*80)
        try:
            node.observation = float(response)
            node.finished = (node.observation >= 1.0)
        except ValueError:
            pass
        show_compact(f'evaluate: {node.observation}', node)

    def simulate(self, node: Node):
        # run the agent just along the states
        # consolidate the state of play (or success|failure) into the node
        state = node.state
        for i in range(3):
            state_ = step_agent(state)
            if is_done(state_):
                break
            state = state_
        node.state = state  # not sure about this
        node.finished = is_done(state)
        node.observation = 1.0 if node.finished else 0.0
        node.subcount = count_steps(state)  
        show_compact('simulate', node)

    def reflection(self, node: Node):
        show_compact('reflection', node)
        
    # utils
    def show_end_state(self):
        print(f'cache hits: {cache.hits}')


App = Agent

if __name__ == "__main__":
    pass
