import unittest

from sonic_pi_code_generator.lib.ast import StatementSequence, UseSynth


class MyTestCase(unittest.TestCase):
    def test_render_empty_statement_sequence(self):
        sequence = StatementSequence()
        sequence.statements = []
        lines = sequence.render_as_lines()
        self.assertEqual([], lines)

    def test_use_synths(self):
        sequence = StatementSequence()
        sequence.statements = [
            UseSynth(synth_name=":tb303"),
            UseSynth(synth_name=":tb303")
        ]

        lines = sequence.render_as_lines()
        self.assertEqual(['use synth :tb303', 'use synth :tb303'], lines)


if __name__ == '__main__':
    unittest.main()
