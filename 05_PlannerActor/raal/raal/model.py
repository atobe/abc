from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple


@dataclass
class Context:
    pass


@dataclass
class Tool:
    context: Context


@dataclass
class AgentState:
    prompt: str
    tools: List[type]
    system_prompt: str
    context: Optional[Context] = None
    plan: Optional[str] = None
    finished: bool = False
    prior_state: Optional["AgentState"] = None
    chunks: List["Chunk"] = field(default_factory=list)

    def clone(self):
        return AgentState(
            prompt=self.prompt,
            tools=self.tools,
            system_prompt=self.system_prompt,
            context=self.context,
            plan=self.plan,
            finished=self.finished,
            prior_state=self.prior_state,
            chunks=self.chunks.copy(),
        )


@dataclass
class FunctionCall:
    function_name: str
    args: List[str]
    kwargs: Dict[str, Any]
    heredoc: Optional[str] = None


@dataclass
class Chunk:
    text: str
    original_text: str = ''


@dataclass
class Thought(Chunk):
    pass


@dataclass
class Action:
    function_call: FunctionCall
    original_text: str


@dataclass
class Observation(Chunk):
    def __post_init__(self):
        self.original_text = 'Observation: ' + self.text


@dataclass
class Answer(Chunk):
    pass


@dataclass
class FunctionSignature:
    name: str
    args: List[Tuple[str, str, str]]  # name/type/default
    # return_type: Optional[str] = None


@dataclass
class ThoughtActionObservation:
    thought: Thought
    action: Action
    observation: Observation


@dataclass
class ToolExposition:
    name: str
    description: str
    signature: FunctionSignature
    examples: List[ThoughtActionObservation] = field(default_factory=list)


@dataclass
class ToolContext:
    project: Context


class NO_DEFAULT:
    pass
