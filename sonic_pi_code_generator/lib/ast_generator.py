from sonic_pi_code_generator.lib.ast import ASTNode, StatementSequence, UseSynth, Define, StringLiteral, WithFx, Play


class ASTGenerator:
    def generate(self, complexity: int) -> ASTNode:

        sequence = StatementSequence()

        for i in range(complexity):
            sequence.statements.append(UseSynth(
                synth_name=StringLiteral(value=":tb303")
            ))

        for i in range(complexity):
            sequence.statements.append(
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
                ))

        sequence.statements.append(
            UseSynth(
                synth_name=StringLiteral(value=":5")
            ))

        sequence.statements.append(Play(
            note=StringLiteral(value=str(63))
        ))

        return sequence
