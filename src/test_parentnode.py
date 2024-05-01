import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual('<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>', node.to_html())

    def test_nested_to_html(self):
        node = ParentNode('div', [
            ParentNode("p", [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]),
            ParentNode("div", [
                ParentNode("p", [
                    LeafNode('span', 'Text span'),
                ], {'style': 'font-weight: bold'}),
            ]),
        ], {'class': 'container'})

        self.assertEqual('<div class="container"><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><div><p style="font-weight: bold"><span>Text span</span></p></div></div>', node.to_html())


if __name__ == "__main__":
    unittest.main()

