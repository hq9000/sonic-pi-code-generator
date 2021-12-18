from abc import ABC, abstractmethod
from typing import List, Optional, Type

from sonic_pi_code_generator.lib.raw_ast import RawASTNode, VALUE_EMPTY
import sys

RAW_NODE_TYPE_PREFIX_FOR_SCALARS = 'scalar_'
RAW_NODE_TYPE_PREFIX_FOR_LISTS = 'list_'


class ASTNode(ABC):

    @abstractmethod
    def render_as_lines(self) -> List[str]:
        pass

    @abstractmethod
    def render_as_string(self) -> str:
        pass

    @abstractmethod
    def get_all_property_names(self) -> List[str]:
        pass

    def render_as_raw_ast_node(self) -> RawASTNode:
        this_raw_node = RawASTNode()
        this_raw_node.type = type(self).__name__
        this_raw_node.value = VALUE_EMPTY

        for property_name in self.get_all_property_names():
            parameter_raw_proxy_node = RawASTNode()
            this_raw_node.children.append(parameter_raw_proxy_node)


            parameter_raw_proxy_node.value = VALUE_EMPTY
            parameter_raw_proxy_node.parent = this_raw_node

            property_value = getattr(self, property_name)

            assert (isinstance(property_value, ASTNode) or isinstance(property_value, list))

            if isinstance(property_value, ASTNode):
                list_of_children: List[ASTNode] = [property_value]
                raw_type_prefix = RAW_NODE_TYPE_PREFIX_FOR_SCALARS
            elif isinstance(property_value, list):
                list_of_children: List[ASTNode] = property_value
                raw_type_prefix = RAW_NODE_TYPE_PREFIX_FOR_LISTS
            else:
                raise TypeError()

            parameter_raw_proxy_node.type = raw_type_prefix + property_name

            for children_ast_node in list_of_children:
                property_raw_node = children_ast_node.render_as_raw_ast_node()
                property_raw_node.parent = parameter_raw_proxy_node
                parameter_raw_proxy_node.children.append(property_raw_node)

        return this_raw_node

    def _indent_lines(self, lines: List[str]) -> List[str]:
        return ['  ' + line for line in lines]


class StatementSequence(ASTNode):

    def get_all_property_names(self) -> List[str]:
        return ['statements']

    def render_as_string(self) -> str:
        raise NotImplemented

    def __init__(self, statements: Optional[List[ASTNode]] = None):
        self.statements: List[ASTNode] = [] if statements is None else statements

    def render_as_lines(self) -> List[str]:
        res = []
        for statement in self.statements:
            lines = statement.render_as_lines()
            res += lines

        return res


class UseSynth(ASTNode):

    def get_all_property_names(self) -> List[str]:
        return ['synth_name']

    def __init__(self, synth_name: Optional[ASTNode] = None):
        self.synth_name: Optional[ASTNode] = synth_name

    def render_as_lines(self) -> List[str]:
        return [f"use synth {self.synth_name.render_as_string()}"]

    def render_as_string(self) -> str:
        raise NotImplementedError()

class Define(ASTNode):

    def get_all_property_names(self) -> List[str]:
        return ['name', 'statement_sequence']

    def __init__(self, name: Optional[ASTNode] = None, statement_sequence: Optional[StatementSequence] = None):
        self.name: Optional[ASTNode] = name
        self.statement_sequence: Optional[StatementSequence] = statement_sequence

    def render_as_lines(self) -> List[str]:
        return [
            f"define {self.name.render_as_string()} do",
            *self._indent_lines(self.statement_sequence.render_as_lines()),
            "done"
        ]

    def render_as_string(self) -> str:
        return '\n'.join(self.render_as_lines())


class StringLiteral(ASTNode):

    UNDEFINED = 'undefined'

    def __init__(self, value: str = UNDEFINED):
        self.value: str = value
        pass

    def render_as_lines(self) -> List[str]:
        return [self.render_as_string()]

    def render_as_string(self) -> str:
        return self.value

    def get_all_property_names(self) -> List[str]:
        pass

    def render_as_raw_ast_node(self) -> RawASTNode:
        res = RawASTNode()
        res.type = type(self).__name__
        res.value = self.value
        return res


class ASTNodeFactory:

    def create_ast_node_by_raw(self, raw_node: RawASTNode) -> ASTNode:
        ast_node_class = self.find_ast_node_class(raw_node.type)
        blank_node = ast_node_class()  # type: ASTNode

        if isinstance(blank_node, StringLiteral):
            blank_node.value = raw_node.value
        else:
            for raw_child in raw_node.children:
                raw_property_name = raw_child.type

                if raw_property_name.startswith(RAW_NODE_TYPE_PREFIX_FOR_SCALARS):
                    real_property_name = raw_property_name.replace(RAW_NODE_TYPE_PREFIX_FOR_SCALARS, '')
                    setattr(blank_node, real_property_name, self.create_ast_node_by_raw(raw_child.children[0]))

                elif raw_property_name.startswith(RAW_NODE_TYPE_PREFIX_FOR_LISTS):
                    real_property_name = raw_property_name.replace(RAW_NODE_TYPE_PREFIX_FOR_LISTS, '')

                    to_set_arr = []
                    for raw_subchild in raw_child.children:
                        to_set_arr.append(self.create_ast_node_by_raw(raw_subchild))

                    setattr(blank_node, real_property_name, to_set_arr)
                else:
                    raise Exception()

        return blank_node

    def find_ast_node_class(self, raw_type: str) -> Type:
        return getattr(sys.modules[__name__], raw_type)
