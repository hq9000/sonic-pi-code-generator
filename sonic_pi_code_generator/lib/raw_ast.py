from typing import List, Optional

_UNDEFINED_TYPE = 'undefined'
VALUE_EMPTY = 'EMPTY'


class RawASTNode:
    def __init__(self):
        self.children = []  # type: List[RawASTNode]
        self.parent = None  # type: Optional[RawASTNode]
        self.type: str = _UNDEFINED_TYPE
        self.value: str = VALUE_EMPTY



