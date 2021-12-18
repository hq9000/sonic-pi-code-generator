import unittest

from sonic_pi_code_generator.lib.ast import StatementSequence, UseSynth, StringLiteral
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

        lines = sequence.render_as_lines()
        self.assertEqual(['use synth :tb303'], lines)

        raw_ast = sequence.render_as_raw_ast_node()
        self.assertIsInstance(raw_ast, RawASTNode)
        pass


if __name__ == '__main__':
    unittest.main()
