from lats.apps._base import App
from lats.model import Node, InputNode
from lats.llm import sample_llm
from lats.apps.humaneval.lib import _get_case
from lats.apps.humaneval import test as humaneval_test


first_prompt = """
You are an AI Python assistant. 
You will be given a function signature and a description of the function. 
Write the full implementation of the function.
Only write the code for the function, no test cases, explanations, or other code.

{function}
"""

general_case_prompt1 = """
You are an AI Python assistant. 
You will be given your previous implementation of a function, and a series of unit tests results.
Write a new full implementation (restate the function signature).

{prev_implementation}

{test_feedback}
"""

general_case_prompt2 = """
You are an AI Python assistant. 
You will be given your previous implementation of a function, a series of unit tests results,
and your self-reflection on your previous implementation. 
Write your full implementation (restate the function signature).
"""


class HumanEval(App):
    REQUIRES_CASE = True

    def __init__(self, case_number=None):
        self.case_number = case_number
        self.problems = None

    def get_root_node(self) -> Node:
        print(f"HEV {self.case_number} get_root_node")
        case = _get_case(self.case_number)
        prompt = case["prompt"]

        return InputNode(prompt_or_question=prompt)

    def expand_InputNode(self, node: Node) -> Node:
        function_spec = node.prompt_or_question
        prompt = first_prompt.format(function=function_spec)
        messages = [{"role": "user", "content": prompt}]
        source = sample_llm(messages, temperature=0.7)
        observation, test_feedback = humaneval_test.value(self.case_number, source)
        new_node = Node(
            parent=node,
            messages=messages,
            observation=observation,
            source=source,
            test_feedback=test_feedback,
        )
        return new_node

    def expand_Node(self, node: Node) -> Node:
        prompt = general_case_prompt1.format(
            prev_implementation=node.source, test_feedback=node.test_feedback
        )
        messages = self.gather_messages(node)
        messages.append({"role": "user", "content": prompt})
        source = sample_llm(messages, temperature=0.7)
        observation, test_feedback = humaneval_test.value(self.case_number, source)
        new_node = Node(
            parent=node,
            messages=messages,
            observation=observation,
            source=source,
            test_feedback=test_feedback,
        )
        return new_node

    def evaluate(self, node: Node) -> float:
        pass

    def simulate(self, node: Node):
        pass

    def reflection(self, node: Node):
        pass

    def value(self, node: Node) -> float:
        # use the source of the node and the canonical test cases to evaluate the node
        if node.observation is None:
            return 0.0
        if "passed" in node.observation:
            return 1.0
        return 0.0

    def root_node(self, node):
        current_node = node
        while current_node.parent is not None:
            current_node = current_node.parent
        return current_node

    def gather_messages(self, node):
        current_node = node
        messages = []
        while current_node is not None:
            messages.append(current_node.messages)
            current_node = current_node.parent
        messages.reverse()
        # flatten
        messages = [msg for sublist in messages for msg in sublist]
        return messages


App = HumanEval

if __name__ == "__main__":
    pass
