from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

Message = Dict[str, str]


@dataclass
class Node:
    score: float = field(default=0.0, repr=True)
    N: int = 0
    parent: Optional["Node"] = None
    children: List["Node"] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)
    observation: Optional[str] = None
    source: Optional[str] = None
    test_feedback: Optional[str] = None
    is_terminal: bool = False
    state: Optional[Any] = None # state of agent or environment
    subcount: int = 0

    @property
    def is_leaf(self):
        return len(self.children) == 0

    def __hash__(self):
        return id(self)


@dataclass
class InputNode(Node):
    prompt_or_question: str = ""
