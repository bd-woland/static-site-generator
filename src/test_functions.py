import unittest

from textnode import TextNode
from leafnode import LeafNode
from functions import split_nodes_delimiter


class TestFunctions(unittest.TestCase):
    def test_split_nodes_delimiter_html_nodes(self):
        html_node = LeafNode('a', 'text', {'href': 'test.com'})
        text_node = TextNode('This is text with a **bolded** word', TextNode.TEXT)

        self.assertEqual([
            html_node,
            TextNode("This is text with a ", TextNode.TEXT),
            TextNode("bolded", TextNode.BOLD),
            TextNode(" word", TextNode.TEXT),
            html_node,
        ], split_nodes_delimiter([html_node, text_node, html_node], '**', TextNode.BOLD))

    def test_split_nodes_delimiter_position(self):
        middle_node = TextNode('This is text with a **bolded** word', TextNode.TEXT)
        start_node = TextNode('**Bolded** word is at the start', TextNode.TEXT)
        end_node = TextNode('Bolded word is at the **end**', TextNode.TEXT)

        self.assertEqual([
            TextNode("This is text with a ", TextNode.TEXT),
            TextNode("bolded", TextNode.BOLD),
            TextNode(" word", TextNode.TEXT),
        ], split_nodes_delimiter([middle_node], '**', TextNode.BOLD))

        self.assertEqual([
            TextNode("Bolded", TextNode.BOLD),
            TextNode(" word is at the start", TextNode.TEXT),
        ], split_nodes_delimiter([start_node], '**', TextNode.BOLD))

        self.assertEqual([
            TextNode("Bolded word is at the ", TextNode.TEXT),
            TextNode("end", TextNode.BOLD),
        ], split_nodes_delimiter([end_node], '**', TextNode.BOLD))

    def test_split_nodes_delimiter_multiple(self):
        node_with_spaces = TextNode('This is **text** with multiple **bolded** words', TextNode.TEXT)
        node_without_spaces = TextNode('```code block 1``````code block 2```', TextNode.CODE)

        self.assertEqual([
            TextNode("This is ", TextNode.TEXT),
            TextNode("text", TextNode.BOLD),
            TextNode(" with multiple ", TextNode.TEXT),
            TextNode("bolded", TextNode.BOLD),
            TextNode(" words", TextNode.TEXT),
        ], split_nodes_delimiter([node_with_spaces], '**', TextNode.BOLD))

        self.assertEqual([
            TextNode("code block 1", TextNode.CODE),
            TextNode("code block 2", TextNode.CODE),
        ], split_nodes_delimiter([node_without_spaces], '```', TextNode.CODE))

    def test_split_nodes_delimiter_invalid(self):
        invalid_node = TextNode('This is text with **unclosed delimiter', TextNode.TEXT)

        def split_node():
            split_nodes_delimiter([invalid_node], '**', TextNode.BOLD)

        self.assertRaises(Exception, split_node)

    def test_split_nodes_delimiter_consecutive(self):
        mixed_node = TextNode('This is text with a **bolded** word and an *italic* word', TextNode.TEXT)
        split_nodes = split_nodes_delimiter(
            split_nodes_delimiter([mixed_node], '**', TextNode.BOLD),
            '*',
            TextNode.ITALIC
        )

        self.assertEqual([
            TextNode("This is text with a ", TextNode.TEXT),
            TextNode("bolded", TextNode.BOLD),
            TextNode(" word and an ", TextNode.TEXT),
            TextNode("italic", TextNode.ITALIC),
            TextNode(" word", TextNode.TEXT),
        ], split_nodes)

if __name__ == "__main__":
    unittest.main()

