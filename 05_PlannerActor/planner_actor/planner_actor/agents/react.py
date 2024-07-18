from ..agent import Agent
from raal.tools import WikipediaSearch, Calculator

class ReActAgent(Agent):
    def get_tools(self):
        return [WikipediaSearch, Calculator]
