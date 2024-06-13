# Structure In - Structure Out
from devtools import pprint

class Renderer:
    """Render a nested datastructure down to text"""

    def __init__(self):
        self.text = ""

    def render(self, instance):
        self.visit(instance)
        return self.text

    def visit(self, node):
        return getattr(self, f"visit_{node.__class__.__name__}", self.default)(node)

    def default(self, node):
        # check is instance of a class
        if hasattr(node, "__siso__"):
            self.visit_siso(node)
        elif hasattr(node, "__dict__"):
            self.visit_instance(node)
        else:
            self.visit_default(node)

    def visit_siso(self, node):
        self.text += node.__siso__() + "\n\n"

    def visit_instance(self, instance):
        for field_name, field_value in instance.__dict__.items():
            self.text += f"{field_name}:\n"
            self.visit(field_value)

    def visit_default(self, node):
        self.text += str(node) + "\n\n"

