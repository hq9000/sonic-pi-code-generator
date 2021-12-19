import json
import unittest

from sonic_pi_code_generator.lib.ast_as_json_presenter import ASTAsJsonPresenter
from sonic_pi_code_generator.lib.ast_generator import ASTGenerator


class MyTestCase(unittest.TestCase):
    def test_something(self):
        generator = ASTGenerator()
        ast = generator.generate(1)
        json_presenter = ASTAsJsonPresenter()
        ast_json = json_presenter.present(ast)

        decoded_json = json.loads(ast_json)
        expected_decoded_json = [{'type': 'StatementSequence', 'children': [1]},
                                 {'type': 'list_statements', 'children': [2, 5, 26, 29]},
                                 {'type': 'UseSynth', 'children': [3]}, {'type': 'scalar_synth_name', 'children': [4]},
                                 {'type': 'StringLiteral', 'value': ':tb303'}, {'type': 'Define', 'children': [6, 8]},
                                 {'type': 'scalar_name', 'children': [7]},
                                 {'type': 'StringLiteral', 'value': 'function'},
                                 {'type': 'scalar_statement_sequence', 'children': [9]},
                                 {'type': 'StatementSequence', 'children': [10]},
                                 {'type': 'list_statements', 'children': [11, 14, 17]},
                                 {'type': 'UseSynth', 'children': [12]},
                                 {'type': 'scalar_synth_name', 'children': [13]},
                                 {'type': 'StringLiteral', 'value': ':a'}, {'type': 'UseSynth', 'children': [15]},
                                 {'type': 'scalar_synth_name', 'children': [16]},
                                 {'type': 'StringLiteral', 'value': ':b'}, {'type': 'WithFx', 'children': [18, 20]},
                                 {'type': 'scalar_fx_name', 'children': [19]},
                                 {'type': 'StringLiteral', 'value': ':echo'},
                                 {'type': 'scalar_statement_sequence', 'children': [21]},
                                 {'type': 'StatementSequence', 'children': [22]},
                                 {'type': 'list_statements', 'children': [23]}, {'type': 'Play', 'children': [24]},
                                 {'type': 'scalar_note', 'children': [25]}, {'type': 'StringLiteral', 'value': '65'},
                                 {'type': 'UseSynth', 'children': [27]},
                                 {'type': 'scalar_synth_name', 'children': [28]},
                                 {'type': 'StringLiteral', 'value': ':5'}, {'type': 'Play', 'children': [30]},
                                 {'type': 'scalar_note', 'children': [31]}, {'type': 'StringLiteral', 'value': '63'}]

        self.assertEqual(decoded_json, expected_decoded_json)


if __name__ == '__main__':
    unittest.main()
