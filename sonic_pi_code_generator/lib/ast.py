from abc import ABC, abstractmethod
from typing import List

STATEMENT_SEQUENCE_INDENT = 2


class ASTNode(ABC):
    @abstractmethod
    def render_as_lines(self) -> List[str]:
        pass

    def _indent(self, lines: List[str]) -> List[str]:
        return ['  ' + line for line in lines]


class Expression(ASTNode, ABC):
    pass


class Statement(ASTNode, ABC):
    pass


class StatementSequence(ASTNode):

    def __init__(self, statements: List[Statement] = []):
        self.statements: List[Statement] = statements

    def render_as_lines(self) -> List[str]:
        res = []
        for statement in self.statements:
            lines = statement.render_as_lines()
            res += lines

        return res


class UseSynth(Statement):

    def __init__(self, synth_name: str):
        self.synth_name: str = synth_name

    def render_as_lines(self) -> List[str]:
        return [f"use synth :{self.synth_name}"]


class Define(Statement):
    def __init__(self, name: str, body: StatementSequence):
        self.name: str = name
        self.body: StatementSequence = body

    def render_as_lines(self) -> List[str]:
        return [
            f"define :{self.name} do",
            *self._indent(self.body.render_as_lines()),
            "done"
        ]



class DoBlock(ASTNode):
    pass
