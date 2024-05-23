from llm import turn, MessageType
from prompt import system_prompt
from parser import parse, ActionType
from tools import calculate, wikipedia, simon_blog_search, known_actions
from dataclasses import dataclass, field
from typing import List
from pprint import pprint
from termcolor import colored, cprint

@dataclass
class AgentState:
    messages: List[MessageType] = field(default_factory=list)
    finished: bool = False


def init_agent_state(question):
    cprint(f'Question: ', 'cyan', end='')
    cprint(question, 'white')
    print()

    return AgentState(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ]
    )


def take_action(state: AgentState, action: ActionType) -> AgentState:
    # if there is no action, assume that the agent is finished
    if not action:
        state.finished = True
        return state

    # e.g. action=wikipedia, action_input=Django
    action, action_input = action

    if action not in known_actions:
        raise Exception("Unknown action: {}: {}".format(action, action_input))

    # look up the actual function/tool to call
    action_func = known_actions[action]

    # call the function/tool with the input and get the result
    observation = action_func(action_input)
    print()
    cprint(f"Observation: ", "cyan", end='')
    cprint(observation, "white")
    print()

    # build a new message reporting the result to the agent
    # note the role of user
    observation_message = {
        "role": "user",
        "content":f"Observation: {observation}",
    }

    # update the agent state with the new message
    next_agent_state = AgentState(
        messages=state.messages + [observation_message],
        finished=state.finished,
    )

    return next_agent_state


def run_agent(question, max_turns=20):
    # Start with the system prompt
    # and the user's question
    agent_state = init_agent_state(question)

    for i in range(max_turns):
        # Get the LLM to generate a Thought and Action
        result = turn(agent_state.messages)

        # Add the agent's response to the messages
        agent_state.messages.append({"role": "assistant", "content": result})

        # Parse out the action from the LLM response if there is one
        action = parse(result)

        agent_state = take_action(agent_state, action)

        print()

        if agent_state.finished:
            cprint('Agent finished', 'yellow')
            print()
            
            pprint(agent_state.messages)
            break

        # input()
