from dataclasses import dataclass


@dataclass
class FlatASTElement:
    type: str
    value: str
    has_right_sibling: bool
    has_children: bool
