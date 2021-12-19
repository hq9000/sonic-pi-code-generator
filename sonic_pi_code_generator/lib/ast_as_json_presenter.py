from typing import Any, Dict, List, Union

from sonic_pi_code_generator.lib.ast import ASTNode
from sonic_pi_code_generator.lib.flat_ast import FlatASTElement
from sonic_pi_code_generator.lib.raw_ast import VALUE_EMPTY

import json


class ASTAsJsonPresenter:
    def present(self, ast_node: ASTNode) -> str:
        raw_ast = ast_node.render_as_raw_ast_node()
        flat_ast_elements = raw_ast.render_as_flat_ast_elements()
        res = []
        for flat_element in flat_ast_elements:
            res.append(self._convert_flat_element_to_dict(flat_element))

        return json.dumps(res)

    def _convert_flat_element_to_dict(self, flat_ast_element: FlatASTElement) -> Dict[str, Union[str, List]]:
        res = {
            "type": flat_ast_element.type,
        }

        if flat_ast_element.value != VALUE_EMPTY:
            res["value"] = flat_ast_element.value

        if flat_ast_element.children_positions:
            res["children"] = flat_ast_element.children_positions

        return res
