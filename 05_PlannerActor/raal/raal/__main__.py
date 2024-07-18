from devtools import pprint

from .agent import init_agent, step_agent, is_done, extract_final_answer
from .agentlib import show_chunks_compact
from .tools import WikipediaSearch, Calculator


def main():
    # prompt = "what is the capital of France? Check please."
    prompt = "What is SZA's age squared?"

    tools = [WikipediaSearch, Calculator]

    state = init_agent(prompt, tools)

    while not is_done(state):
        state = step_agent(state)
        show_chunks_compact(state)

    print("Done!")
    print(extract_final_answer(state))


if __name__ == "__main__":
    main()
