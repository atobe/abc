from string import Template
import datetime
from .toolslib import render_tools_prompt

# moa = """
# You work in a loop of (Thought, Action, Observation)*, potentially followed by a final Answer.
# First Think about what you need to do.
# Write an Action that does it. These look like python function calls, with one addition (see Heredocs below).
# I will perform the Action and provide you with an Observation of the result.
# You may continue with this loop until you feel you are done.
# Then report your final Answer.

# = Heredocs =
# If a large string argument is needed, write it in a heredoc string after the function call.
# You can use HEREDOC as a macro argument as follows :-

# Action: WriteFile('file.txt', HEREDOC, force=False)
# def square(x):
#     return x*x
# Observation: <provided by system, you do not write this line>
# The system will inject the heredoc string into the function call.
# """.strip()

# example = """
# Use this example session as a template for your work.
# user said: "write a function that squares a number in nanomath.py"
# Thought: I need to write the square function in nanomath.py
# Action: WriteFile('nanomath.py', HEREDOC, force=False)
# def square(x):
#     return x+x
# Observation: 2 lines written to nanomath.py
# Thought: Oh no, I made a mistake in the function. I need to correct it.
# Action: WriteFile('nanomath.py', HEREDOC, force=True)
# def square(x):
#     return x*x
# Answer: I have written the square function in nanomath.py
# """


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
Thought: I need to set the time
Action: SetTime('20:00:00')
Observation: Time set to 20:00:00
Answer: I have set the time
"""

system_prompt_template = """
$mechanism_of_action

You have the following tools:
$tools
$examples

No need to put triple quotes around the heredoc string. Just write the string as is.
Take one step at a time, Thought then Action.
Only reply with Thought: Action: or Answer: lines.
By the way the date today is {date}.
Be sure to check facts on the web or wikipedia.
Start immediately with a Thought: line.
"""


system_prompt_template = """
$mechanism_of_action

You have the following tools:
$tools
$examples

Take one step at a time, Thought then Action.
Only reply with Thought: Action: or Answer: lines.
Start immediately with a Thought: line.
"""


def render_prompt(tools):
    tools_s = render_tools_prompt(tools)
    date_s = datetime.datetime.now().strftime("%a %d %b %Y")
    template = Template(system_prompt_template)
    return template.substitute(
        mechanism_of_action=moa, tools=tools_s, examples=example, date=date_s
    )
