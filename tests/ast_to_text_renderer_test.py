import unittest

from sonic_pi_code_generator.lib.ast import StatementSequence


class MyTestCase(unittest.TestCase):
    def test_render_empty_statement_sequence(self):
        sequence = StatementSequence()
        sequence.statements = []
        lines = sequence.render_as_lines()
        self.assertEqual([], lines)


if __name__ == '__main__':
    unittest.main()
