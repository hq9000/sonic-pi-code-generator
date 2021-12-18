import unittest

from sonic_pi_code_generator.lib.ast import StatementSequence, UseSynth, Define, Assignment, LValue, StringLiteral, \
    NumericLiteral, Sleep


class MyTestCase(unittest.TestCase):
    def test_render_empty_statement_sequence(self):
        sequence = StatementSequence([])
        sequence.statements = []
        lines = sequence.render_as_lines()
        self.assertEqual([], lines)

    def test_different_nodes(self):
        sequence = StatementSequence([
            UseSynth(synth_name="tb303"),
            UseSynth(synth_name="tb303"),
            Define(
                name='define_name',
                body=StatementSequence(statements=[
                    UseSynth(synth_name="xxx"),
                    UseSynth(synth_name="yyy")
                ]))
        ]
        )

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

    def test_assignment(self):
        assignment_with_string_literal = Assignment(
            LValue('x'),
            StringLiteral("abc")
        )

        lines = assignment_with_string_literal.render_as_lines()
        self.assertEqual(['x = abc'], lines)

        assignment_with_numeric_literal = Assignment(
            LValue('x'),
            NumericLiteral(123)
        )

        lines = assignment_with_numeric_literal.render_as_lines()
        self.assertEqual(['x = 123'], lines)

    def test_sleep(self):
        sleep = Sleep(duration=1.23)
        self.assertEqual(
            ['sleep 1.23'], sleep.render_as_lines()
        )


if __name__ == '__main__':
    unittest.main()
