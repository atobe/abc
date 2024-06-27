import importlib.util
from pathlib import Path
from lats.model import Node


class App:
    """An application of LATS to some task or eval"""

    def get_root_node(self) -> Node:
        return None

    def expand_InputNode(self, node: Node) -> Node:
        return None

    def expand_Node(self, node: Node) -> Node:
        return None

    def evaluate(self, node: Node) -> float:
        pass

    def simulate(self, node: Node):
        pass

    def reflection(self, node: Node):
        pass
    
    # utils
    def show_end_state(self):
        pass


def get_app_by_name(app_name) -> App:
    apps_dir = Path(__file__).parent
    # apps may be .../apps/app_name.py
    # or          .../apps/app_name/__init__.py
    # so deal with both
    module_path = apps_dir / f"{app_name}.py"
    if not module_path.exists():
        module_path = apps_dir / app_name / "__init__.py"
    if not module_path.exists():
        raise FileNotFoundError(f"Could not find app {app_name}")
    spec = importlib.util.spec_from_file_location(app_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.App


if __name__ == "__main__":
    print(get_app_by_name("humaneval"))
