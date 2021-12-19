from typing import List, Optional

from sonic_pi_code_generator.lib.flat_ast import FlatASTElement

_UNDEFINED_TYPE = 'undefined'
VALUE_EMPTY = 'EMPTY'


class RawASTNode:
    def __init__(self, raw_type: str = _UNDEFINED_TYPE, value: str = VALUE_EMPTY):
        self.children = []  # type: List[RawASTNode]
        self.parent = None  # type: Optional[RawASTNode]
        self.type: str = raw_type
        self.value: str = value

        # used when converting flat to raw
        self.flat_ast_element: Optional[FlatASTElement] = None

    def set_children(self, new_children):
        # type: (List[RawASTNode])->None
        self.children = new_children
        for child in self.children:
            child.parent = self

    def add_child(self, new_child):
        # type: (RawASTNode)->None
        self.children.append(new_child)
        new_child.parent = self

    def render_as_flat_ast_elements(self, position_as_list: Optional[List[int]] = None) -> List[FlatASTElement]:
        # essentially it's an "in-order depth first traversal"
        # with putting "has children"
        # and "has right sibling" markers
        # as requested by https://arxiv.org/pdf/1711.09573.pdf

        if position_as_list is None:
            position_as_list = [0]

        top_element = FlatASTElement(
            position=position_as_list[0],  # position_as_list is passed as a list of one element in order to be mutable
            type=self.type,
            value=self.value,
            has_children=self.has_children(),
            has_right_sibling=self.has_right_sibling(),
            children_positions=[]
        )

        res = [top_element]

        position_as_list[0] += 1

        for child in self.children:
            top_element.children_positions.append(position_as_list[0])
            flat_child_elements = child.render_as_flat_ast_elements(position_as_list)
            res += flat_child_elements

        return res

    def has_children(self) -> bool:
        return len(self.children) > 0

    def has_right_sibling(self) -> bool:
        if self.parent is None:
            return False

        for i, child in enumerate(parents_children := self.parent.children):
            if child is self:
                if i < len(parents_children) - 1:
                    return True
                else:
                    return False
        raise Exception('new_node not found among its parent\'s children')


class RawASTNodeFactory:
    def construct_from_list_of_flat_elements(self, flat_elements: List[FlatASTElement]) -> RawASTNode:
        last_created_node: Optional[RawASTNode] = None
        root_node: Optional[RawASTNode] = None

        for flat_element in flat_elements:
            new_node = self._create_not_connected_node(flat_element)
            self._connect_new_node(new_node, last_created_node)
            if last_created_node is None:
                root_node = new_node

            last_created_node = new_node

        if root_node is None:
            raise Exception('root node not found')

        return root_node

    def _create_not_connected_node(self, flat_element: FlatASTElement) -> RawASTNode:
        res = RawASTNode()
        res.type = flat_element.type
        res.value = flat_element.value
        res.flat_ast_element = flat_element
        return res

    def _connect_new_node(self, new_node: RawASTNode, last_created_node: Optional[RawASTNode]):
        if last_created_node is None:
            return

        if last_created_node.flat_ast_element.has_children:
            parent = last_created_node
        elif last_created_node.flat_ast_element.has_right_sibling:
            parent = last_created_node.parent
        else:
            parent = self._find_closes_parent_with_right_sibling(last_created_node)

        parent.add_child(new_node)

    def _find_closes_parent_with_right_sibling(self, last_created_node: RawASTNode) -> RawASTNode:
        cursor = last_created_node

        while not cursor.flat_ast_element.has_right_sibling:
            if cursor.parent is None:
                raise Exception('reached the top and not found a parent to connect to!')

            cursor = cursor.parent

        # we have found the guy with a right sibling,
        # so we need to return its parent
        return cursor.parent
