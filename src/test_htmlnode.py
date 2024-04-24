import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={'href': 'https://google.com', 'target': '_blank'})
        node2 = HTMLNode(props={'style': 'display: none; width: 100%', 'class': 'd-none w-100', 'data-target': '#target'})

        self.assertEqual('href="https://google.com" target="_blank"', node.props_to_html())
        self.assertEqual('style="display: none; width: 100%" class="d-none w-100" data-target="#target"', node2.props_to_html())

    def test_empty_props(self):
        node = HTMLNode(props={})
        node2 = HTMLNode()

        self.assertEqual('', node.props_to_html())
        self.assertEqual('', node2.props_to_html())


if __name__ == "__main__":
    unittest.main()

