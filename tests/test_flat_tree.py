import unittest
from typing import List, Dict

from sonic_pi_code_generator.lib.flat_ast import FlatASTElement
from sonic_pi_code_generator.lib.raw_ast import RawASTNode, RawASTNodeFactory


class MyTestCase(unittest.TestCase):
    def test_something(self):
        """
        the tree here is this one:
        https://user-images.githubusercontent.com/21345604/146665558-db526b13-d729-4548-a44f-a5388252acf2.png

        """
        root_node = RawASTNode('t', '1')
        node2 = RawASTNode('t', '2')
        node3 = RawASTNode('t', '3')
        node4 = RawASTNode('t', '4')
        node5 = RawASTNode('t', '5')
        node6 = RawASTNode('t', '6')
        node7 = RawASTNode('t', '7')
        node8 = RawASTNode('t', '8')

        root_node.set_children([node2, node8, node5])
        node2.set_children([node3, node7, node4])
        node3.set_children([node6])

        flat_elements = root_node.render_as_flat_ast_elements()
        digest_before = self._create_flat_elements_digest(flat_elements)

        self.assertEqual(digest_before,
                         [{'p': 0, 't': 't', 'v': '1', 'c': '1', 'rs': '0', 'cp': [1, 6, 7]},
                          {'p': 1, 't': 't', 'v': '2', 'c': '1', 'rs': '1', 'cp': [2, 4, 5]},
                          {'p': 2, 't': 't', 'v': '3', 'c': '1', 'rs': '1', 'cp': [3]},
                          {'p': 3, 't': 't', 'v': '6', 'c': '0', 'rs': '0', 'cp': []},
                          {'p': 4, 't': 't', 'v': '7', 'c': '0', 'rs': '1', 'cp': []},
                          {'p': 5, 't': 't', 'v': '4', 'c': '0', 'rs': '0', 'cp': []},
                          {'p': 6, 't': 't', 'v': '8', 'c': '0', 'rs': '1', 'cp': []},
                          {'p': 7, 't': 't', 'v': '5', 'c': '0', 'rs': '0', 'cp': []}])

        self.assertEqual(len(flat_elements), 8)

        factory = RawASTNodeFactory()

        restored_raws = factory.construct_from_list_of_flat_elements(flat_elements)
        flat_elements_after = restored_raws.render_as_flat_ast_elements()
        digest_after = self._create_flat_elements_digest(flat_elements_after)

        self.assertEqual(digest_after, digest_before)

    def _create_flat_elements_digest(self, flat_elements: List[FlatASTElement]) -> List[Dict[str, str]]:
        res = []
        for element in flat_elements:
            res.append({
                "p": element.position,
                "t": element.type,
                "v": element.value,
                "c": "1" if element.has_children else "0",
                "rs": "1" if element.has_right_sibling else "0",
                "cp": element.children_positions
            })

        return res


if __name__ == '__main__':
    unittest.main()
