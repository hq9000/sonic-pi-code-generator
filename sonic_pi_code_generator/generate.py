import argparse

from sonic_pi_code_generator.lib.ast_as_json_presenter import ASTAsJsonPresenter
from sonic_pi_code_generator.lib.ast_generator import ASTGenerator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates flat ASTs of synthetic Sonic Pi programs as a json file')

    parser.add_argument('--complexity',
                        type=int,
                        help='complexity level 1+')

    parser.add_argument('--num_programs',
                        type=int,
                        help='number of programs 1+')

    parser.add_argument('--out_file',
                        type=str,
                        help='place to put json data to')

    args = parser.parse_args()

    complexity: int = args.complexity
    num_programs: int = args.num_programs
    out_file_path: str = args.out_file

    if type(complexity) != int or complexity <= 0:
        raise Exception('complexity is wrong')

    if type(num_programs) != int or num_programs <= 0:
        raise Exception('num_programs is wrong')

    generator = ASTGenerator()
    presenter = ASTAsJsonPresenter()

    with open(out_file_path, "w") as outfile:
        for i in range(num_programs):
            ast = generator.generate(complexity)
            json = presenter.present(ast)
            outfile.write(json)
            outfile.write('\n')

