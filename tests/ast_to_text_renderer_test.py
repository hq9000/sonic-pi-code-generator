import unittest

from sonic_pi_code_generator.lib.ast import StatementSequence, UseSynth, StringLiteral, ASTNodeFactory
from sonic_pi_code_generator.lib.raw_ast import RawASTNode


class MyTestCase(unittest.TestCase):

    def test_whatever(self):
        sequence = StatementSequence(
            [
                UseSynth(
                    synth_name=StringLiteral(value=":tb303")
                )
            ]
        )

        lines_before = sequence.render_as_lines()
        self.assertEqual(['use synth :tb303'], lines_before)

        raw_ast = sequence.render_as_raw_ast_node()
        self.assertIsInstance(raw_ast, RawASTNode)

        ast_factory = ASTNodeFactory()

        restored = ast_factory.create_ast_node_by_raw(raw_ast)
        lines_after = restored.render_as_lines()

        self.assertEqual(lines_before, lines_after)


if __name__ == '__main__':
    unittest.main()
