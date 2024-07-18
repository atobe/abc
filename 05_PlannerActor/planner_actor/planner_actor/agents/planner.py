from ..agent import Agent
from raal.tools import WikipediaSearch, Calculator, RevisePlan, AssignSubtaskToWorker
from string import Template
import datetime
from raal.toolslib import render_tools_prompt

moa = """You work in a loop of (Thought, Action, Observation)*, potentially followed by a final Answer.
First Think about what you need to do.
Write an Action that does it. These look like python function calls.
I will perform the Action and provide you with an Observation of the result.
You may continue with this loop until you feel you are done. 
Then report your final Answer.

""".strip()

example = """
Use this example session as a template for your work.
user said: "oh the power went out, set the time to 8pm"
Thought: I need to make a plan
Action: RevisePlan('- [ ] Set the time to 8pm\n- [ ] Check the time\n')
Observation: Plan revised. 2 steps.
Thought: I need to set the time
Action: SetTime('20:00:00')
Observation: Time set to 20:00:00
Thought: I need to check the time
Action: CheckTime()
Observation: The time is 20:00:00
Answer: I have set the time correctly
"""


system_prompt_template = """
$mechanism_of_action

You have the following tools:
$tools
$examples

Your plan is currently:
$plan

Take one step at a time, Thought then Action.
Only reply with Thought: Action: or Answer: lines.
Start immediately with a Thought: line.
"""

# By the way the date today is {date}.


def render_prompt(tools, plan):
    tools_s = render_tools_prompt(tools)
    date_s = datetime.datetime.now().strftime("%a %d %b %Y")
    template = Template(system_prompt_template)
    return template.substitute(
        mechanism_of_action=moa, tools=tools_s, examples=example, date=date_s, plan=plan
    )


class PlannerAgent(Agent):
    UPDATES_SYSTEM_PROMPT = True

    def get_tools(self):
        # return [WikipediaSearch, Calculator, RevisePlan]
        return [RevisePlan, AssignSubtaskToWorker]

    def get_system_prompt(self):
        return render_prompt(self.tools, self.state.plan)
