from dataclasses import dataclass
from typing import List


@dataclass
class FlatASTElement:
    position: int
    type: str
    value: str
    has_right_sibling: bool
    has_children: bool
    children_positions: List[int]
