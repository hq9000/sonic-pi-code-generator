from abc import ABC, abstractmethod
from typing import List, Union, Optional, Type

from sonic_pi_code_generator.lib.raw_ast import RawASTNode, VALUE_EMPTY
import sys

RAW_NODE_TYPE_PREFIX_FOR_SCALARS = 'scarlar_'
RAW_NODE_TYPE_PREFIX_FOR_ARRAYS = 'array_'


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

            parameter_raw_proxy_node.type = property_name
            parameter_raw_proxy_node.value = VALUE_EMPTY
            parameter_raw_proxy_node.parent = this_raw_node

            property_value = getattr(self, property_name)

            assert (isinstance(property_value, ASTNode) or isinstance(property_value, list))

            if isinstance(property_value, ASTNode):
                list_of_children: List[ASTNode] = [property_value]
            elif isinstance(property_value, list):
                list_of_children: List[ASTNode] = property_value
            else:
                raise TypeError()

            for children_ast_node in list_of_children:
                property_raw_node = children_ast_node.render_as_raw_ast_node()
                property_raw_node.parent = parameter_raw_proxy_node
                parameter_raw_proxy_node.children.append(property_raw_node)

        return this_raw_node


class StatementSequence(ASTNode):

    def get_all_property_names(self) -> List[str]:
        return ['statements']

    def render_as_string(self) -> str:
        raise NotImplemented

    def __init__(self, statements: List[ASTNode]):
        self.statements: List[ASTNode] = statements

    def render_as_lines(self) -> List[str]:
        res = []
        for statement in self.statements:
            lines = statement.render_as_lines()
            res += lines

        return res


class UseSynth(ASTNode):

    def get_all_property_names(self) -> List[str]:
        return ['synth_name']

    def __init__(self):
        self.synth_name: Optional[ASTNode] = None

    def render_as_lines(self) -> List[str]:
        return [f"use synth {self.synth_name.render_as_string()}"]

    def render_as_string(self) -> str:
        raise NotImplementedError()



class StringLiteral(ASTNode):

    def __init__(self, value: str):
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

                elif raw_property_name.startswith(RAW_NODE_TYPE_PREFIX_FOR_ARRAYS):
                    real_property_name = raw_property_name.replace(RAW_NODE_TYPE_PREFIX_FOR_ARRAYS, '')

                    to_set_arr = []
                    for raw_subchild in raw_child.children:
                        to_set_arr.append = self.create_ast_node_by_raw(raw_subchild)

                    setattr(blank_node, real_property_name, to_set_arr)
                else:
                    raise Exception()

        return blank_node

    def find_ast_node_class(self, raw_type: str) -> Type:
        return getattr(sys.modules[__name__], raw_type)
