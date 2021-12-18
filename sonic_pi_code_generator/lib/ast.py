from abc import ABC, abstractmethod
from typing import List

STATEMENT_SEQUENCE_INDENT = 2


class ASTNode(ABC):
    @abstractmethod
    def render_as_lines(self) -> List[str]:
        pass


class Expression(ASTNode, ABC):
    pass


class Statement(ASTNode, ABC):
    pass


class StatementSequence(ASTNode):

    def __init__(self):
        self.statements: List[Statement] = []

    def render_as_lines(self) -> List[str]:
        res = []
        for statement in self.statements:
            indent = ''
            if isinstance(statement, StatementSequence):
                indent = '  '

            lines = statement.render_as_lines()

            if not indent:
                # no additional indentation needed
                res += lines
            else:
                res += [indent + line for line in lines]

        return res


class DoBlock(ASTNode):
    pass
