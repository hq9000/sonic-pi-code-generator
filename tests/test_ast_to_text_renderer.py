import unittest

from sonic_pi_code_generator.lib.ast import StatementSequence, UseSynth, StringLiteral, ASTNodeFactory, Define, Play, \
    WithFx
from sonic_pi_code_generator.lib.raw_ast import RawASTNode


class MyTestCase(unittest.TestCase):

    def test_whatever(self):
        sequence = StatementSequence(
            [
                UseSynth(
                    synth_name=StringLiteral(value=":tb303")
                ),
                Define(
                    name=StringLiteral(value="function"),
                    statement_sequence=StatementSequence(
                        [
                            UseSynth(
                                synth_name=StringLiteral(value=":a")
                            ),
                            UseSynth(
                                synth_name=StringLiteral(value=":b")
                            ),
                            WithFx(
                                fx_name=StringLiteral(value=":echo"),
                                statement_sequence=StatementSequence([
                                    Play(note=StringLiteral('65'))
                                ])
                            )
                        ]
                    )
                ),
                UseSynth(
                    synth_name=StringLiteral(value=":5")
                ),
                Play(
                    note=StringLiteral(value=str(63))
                )
            ]
        )

        lines_before = sequence.render_as_lines()
        self.assertEqual([
            'use synth :tb303',
            'define function do',
            '  use synth :a',
            '  use synth :b',
            '  with :echo',
            '    play 65',
            '  done',
            'done',
            'use synth :5',
            'play 63'
        ], lines_before)

        raw_ast = sequence.render_as_raw_ast_node()

        flat_ast = raw_ast.render_as_flat_ast_elements()
        self.assertGreater(len(flat_ast), 20)

        self.assertIsInstance(raw_ast, RawASTNode)

        ast_factory = ASTNodeFactory()

        restored = ast_factory.create_ast_node_by_raw(raw_ast)
        lines_after = restored.render_as_lines()

        self.assertEqual(lines_before, lines_after)



if __name__ == '__main__':
    unittest.main()
