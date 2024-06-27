from ..model import Tool, Observation


class Calculator(Tool):
    """Calculate simple mathematical expressions. e.g. 1237 + 24 / 6"""

    def __call__(self, expression: str):
        result = eval(str(expression))
        return Observation(str(result))
