import re
from typing import Tuple, Optional

ActionType = Tuple[str, str]

def parse(response) -> Optional[ActionType]:
    """e.g. Action: wikipedia: Django -> search wikipedia for Django"""
    action_re = re.compile("^Action: (\w+): (.*)$")

    actions = [action_re.match(a) for a in response.split("\n") if action_re.match(a)]
    if actions:
        action, action_input = actions[0].groups()
        return action, action_input
