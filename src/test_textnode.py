import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")

        self.assertEqual(node, node2)
        self.assertEqual(node2, node)

    def test_not_eq_if_text_differs(self):
        node = TextNode('text 1', 'bold')
        node2 = TextNode('text 2', 'bold')

        self.assertNotEqual(node, node2)
        self.assertNotEqual(node2, node)

    def test_not_eq_if_type_differs(self):
        node = TextNode('text', 'bold')
        node2 = TextNode('text', 'italic')

        self.assertNotEqual(node, node2)
        self.assertNotEqual(node2, node)

    def test_not_eq_if_url_differs(self):
        node = TextNode('text', 'bold', 'google.com')
        node2 = TextNode('text', 'bold', 'boot.dev')
        node3 = TextNode('text', 'bold')

        self.assertNotEqual(node, node2)
        self.assertNotEqual(node2, node)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node3, node)

    def test_url_defaults_to_none(self):
        node = TextNode('text', 'bold')
        node2 = TextNode('text', 'bold', None)

        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()

