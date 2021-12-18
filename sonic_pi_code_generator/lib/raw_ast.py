from typing import List, Optional

from sonic_pi_code_generator.lib.flat_ast import FlatASTElement

_UNDEFINED_TYPE = 'undefined'
VALUE_EMPTY = 'EMPTY'


class RawASTNode:
    def __init__(self):
        self.children = []  # type: List[RawASTNode]
        self.parent = None  # type: Optional[RawASTNode]
        self.type: str = _UNDEFINED_TYPE
        self.value: str = VALUE_EMPTY

    def render_as_flat_ast_elements(self) -> List[FlatASTElement]:
        # essentially it's "in-order depth first traversal"
        # with putting "has children"
        # and "has right sibling" markers
        # as requested by https://arxiv.org/pdf/1711.09573.pdf
        res = [FlatASTElement(
            type=self.type,
            value=self.value,
            has_children=self.has_children(),
            has_right_sibling=self.has_right_sibling()
        )]

        for child in self.children:
            res += child.render_as_flat_ast_elements()

    def has_children(self) -> bool:
        return len(self.children) > 0

    def has_right_sibling(self) -> bool:
        for i, child in enumerate(parents_children := self.parent.children):
            if child is self:
                if i < len(parents_children) - 1:
                    return True
                else:
                    return False
        raise Exception('child not found among its parent\'s children')


class RawASTNodeFactory
