from typing import List
import copy
from .model import AgentState, Tool, Action, Answer, Observation
from .prompt import render_prompt
from .agentlib import compile_messages, chunks_to_messages
from .llm import call_llm
from .parser import Parser
from .toolslib import execute_action


def init_agent(prompt: str, tools: List[Tool]) -> AgentState:
    system_prompt = render_prompt(tools)
    return AgentState(prompt=prompt, tools=tools, system_prompt=system_prompt)


def step_agent(state: AgentState) -> AgentState:
    # gather messages
    messages = compile_messages(state)

    # call the llm
    response = call_llm(messages, temperature=0.7)

    new_state = copy.deepcopy(state)
    new_state.prior_state = state

    # parse the result
    observation = None
    try:
        chunks = Parser().parse(response)
        new_state.chunks = chunks
    except Exception as e:
        observation = Observation(text=str(e))

    # error parsing case
    if observation:
        new_state.chunks.append(observation)
        return new_state

    if isinstance(chunks[-1], Action):
        try:
            observation = execute_action(chunks[-1], state.context, state.tools)
        except Exception as e:
            # error executing action
            observation = Observation(text=str(e))
        if observation:
            new_state.chunks.append(observation)

    if isinstance(chunks[-1], Answer):
        new_state.finished = True

    return new_state


def extract_messages(state: AgentState, all_messages=False, trim=0) -> List[str]:
    # trim = 0 to include all messages
    # trim = 1 to remove system prompt
    # trim = 2 to remove system prompt and user prompt
    if all_messages:
        messages = compile_messages(state)
    else:
        messages = chunks_to_messages(state.chunks)
    return messages[trim:]


def is_done(state: AgentState) -> bool:
    return state.finished


def extract_final_answer(state: AgentState) -> str:
    assert isinstance(state.chunks[-1], Answer)
    return state.chunks[-1].text

