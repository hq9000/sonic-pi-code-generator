from abc import ABC, abstractmethod
from typing import List, Union


class ASTNode(ABC):
    pass


class Expression(ASTNode, ABC):
    @abstractmethod
    def render_as_string(self) -> str:
        pass


class Statement(ASTNode, ABC):
    @abstractmethod
    def render_as_lines(self) -> List[str]:
        pass

    def _indent(self, lines: List[str]) -> List[str]:
        return ['  ' + line for line in lines]


class StatementSequence(ASTNode):

    def __init__(self, statements: List[Statement]):
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


class LValue(Expression):

    def __init__(self, name: str):
        self.name: str = name

    def render_as_string(self) -> str:
        return self.name

class StringLiteral(Expression):
    def __init__(self, value: str):
        self.value: str = value

    def render_as_string(self) -> str:
        return self.value


class NumericLiteral(Expression):
    def __init__(self, value: Union[str, float]):
        self.value: Union[str, float] = value

    def render_as_string(self) -> str:
        return str(self.value)


class Assignment(Statement):

    def __init__(self, lvalue: LValue, rvalue: Expression):
        self.lvalue: LValue = lvalue
        self.rvalue: Expression = rvalue

    def render_as_lines(self) -> List[str]:
        return [
            self.lvalue.render_as_string() + " = " + self.rvalue.render_as_string()
        ]
