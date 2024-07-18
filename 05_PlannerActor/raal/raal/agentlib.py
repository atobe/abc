from typing import List, Dict
from .model import Chunk, Thought, Action, AgentState
from termcolor import colored, cprint

def chunks_to_messages(chunks: List[Chunk]) -> List[Dict]:
    messages = []
    last_chunk_type = None
    for chunk in chunks:
        if last_chunk_type == Thought and isinstance(chunk, Action):
            messages[-1]["content"] += "\n" + chunk.original_text
        else:
            role = "assistant" if isinstance(chunk, (Thought, Action)) else "user"
            messages.append({"role": role, "content": chunk.original_text})
        last_chunk_type = type(chunk)
    # pprint(messages)
    return messages


def gather_chunks(state: AgentState) -> List[Chunk]:
    # recursively gather chunks from prior states, then put them in order
    chunks = []
    prior_state = state
    while prior_state:
        chunks = prior_state.chunks + chunks
        prior_state = prior_state.prior_state
    return chunks


def compile_messages(state: AgentState) -> List[Dict]:
    return [
        {"role": "system", "content": state.system_prompt},
        {"role": "user", "content": state.prompt},
    ] + chunks_to_messages(gather_chunks(state))


def get_terminal_width():
    import os

    return os.get_terminal_size().columns


def show_chunks_compact(state: AgentState, rollup=False, indent="", prefix="", color='white'):
    width = get_terminal_width()
    chunks = gather_chunks(state) if rollup else state.chunks
    for chunk in chunks:
        role = "asst" if isinstance(chunk, (Thought, Action)) else "user"
        width -= len(prefix) + len(role) + 2 + len(indent)
        cprint(f"{indent}{prefix}{role} {str(chunk)[:width]}", color)


def trim_chunks(chunks: List[Chunk]) -> List[Chunk]:
    # only keep last 9
    return chunks[-9:]


def count_steps(state: AgentState) -> int:
    return len(gather_chunks(state))
