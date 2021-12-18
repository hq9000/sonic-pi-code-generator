import unittest

from sonic_pi_code_generator.lib.ast import StatementSequence, UseSynth, Define


class MyTestCase(unittest.TestCase):
    def test_render_empty_statement_sequence(self):
        sequence = StatementSequence()
        sequence.statements = []
        lines = sequence.render_as_lines()
        self.assertEqual([], lines)

    def test_different_nodes(self):
        sequence = StatementSequence()

        sequence.statements = [
            UseSynth(synth_name="tb303"),
            UseSynth(synth_name="tb303"),
            Define(
                name='define_name',
                body=StatementSequence(statements=[
                    UseSynth(synth_name="xxx"),
                    UseSynth(synth_name="yyy")
                ]))
        ]

        lines = sequence.render_as_lines()

        expected_lines = [
            'use synth :tb303',
            'use synth :tb303',
            'define :define_name do',
            '  use synth :xxx',
            '  use synth :yyy',
            'done'
        ]

        self.assertEqual(expected_lines, lines)


if __name__ == '__main__':
    unittest.main()
