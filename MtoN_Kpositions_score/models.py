from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from datetime import datetime

#frozen equals true will make dataclass hashable so it can be used as a key
@dataclass
class Professor:
    name: str
    positions: int
    # preflist: List["Student"] = field(default_factory=list)
    positions_open: int = field(init=False)
    # currentpositions: List[Optional["Student"]] = field(init=False)
    currentpositions: List[Optional[Tuple["Student", int]]] = field(init=False)
    interest_score_list: List[int] = field(default_factory=list)
    open: bool = field(init=False)

    def __post_init__(self):
        self.positions_open = self.positions
        self.positions_closed = 0
        self.currentpositions = [None] * self.positions
        self.open = True

    def __repr__(self):
        return f"Prof({self.name})"

@dataclass
class Student:
    name: str
    # preflist: List[Professor] = field(default_factory=list)
    pairedwith: Optional[Professor] = None
    interest_score_list: List[int] = field(default_factory=list)
    # request_date:

    def __repr__(self):
        return f"Student({self.name})"

        