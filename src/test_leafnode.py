import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        text = LeafNode(value='text')
        paragraph = LeafNode("p", "This is a paragraph of text.")
        link = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual('text', text.to_html())
        self.assertEqual('<p>This is a paragraph of text.</p>', paragraph.to_html())
        self.assertEqual('<a href="https://www.google.com">Click me!</a>', link.to_html())

    def test_value_is_required(self):
        def create_node():
            LeafNode(value=None)

        self.assertRaises(ValueError, create_node)


if __name__ == "__main__":
    unittest.main()

