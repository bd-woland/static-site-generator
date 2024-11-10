import unittest

from textnode import TextNode
from leafnode import LeafNode
from functions import (split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, markdown_to_html_node, extract_title)
from parentnode import ParentNode

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
        node_without_spaces = TextNode('`code block 1``code block 2`', TextNode.TEXT)

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
        ], split_nodes_delimiter([node_without_spaces], '`', TextNode.CODE))

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

    def test_extract_markdown_images(self):
        text_without_images = "This is text without images"
        text_with_images = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"

        self.assertEqual([], extract_markdown_images(text_without_images))
        self.assertEqual([
            ('image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png'),
            ('another', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png'),
        ], extract_markdown_images(text_with_images))

    def test_extract_markdown_links(self):
        text_without_links = "This is text without links"
        text_with_links =  "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        text_with_link_and_image =  "This is text with a [link](https://www.example.com) and an ![image](https://www.example.com/image.jpg)"

        self.assertEqual([], extract_markdown_links(text_without_links))
        self.assertEqual([
            ('link', 'https://www.example.com'),
            ('another', 'https://www.example.com/another'),
        ], extract_markdown_links(text_with_links))
        self.assertEqual([
            ('link', 'https://www.example.com'),
        ], extract_markdown_links(text_with_link_and_image))

    def test_split_nodes_image(self):
        node = TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)", TextNode.TEXT)

        self.assertEqual([
            TextNode("This is text with an ", TextNode.TEXT),
            TextNode("image", TextNode.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", TextNode.TEXT),
            TextNode("second image", TextNode.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        ], split_nodes_image([node]))

    def test_split_nodes_link(self):
        node = TextNode("This is text with a [link](http://test.com) and another [second link](https://boot.dev)", TextNode.TEXT)

        self.assertEqual([
            TextNode("This is text with a ", TextNode.TEXT),
            TextNode("link", TextNode.LINK, "http://test.com"),
            TextNode(" and another ", TextNode.TEXT),
            TextNode("second link", TextNode.LINK, "https://boot.dev"),
        ], split_nodes_link([node]))

    def test_text_to_textnodes(self):
        text = 'This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)'

        self.assertEqual([
            TextNode("This is ", TextNode.TEXT),
            TextNode("text", TextNode.BOLD),
            TextNode(" with an ", TextNode.TEXT),
            TextNode("italic", TextNode.ITALIC),
            TextNode(" word and a ", TextNode.TEXT),
            TextNode("code block", TextNode.CODE),
            TextNode(" and an ", TextNode.TEXT),
            TextNode("image", TextNode.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextNode.TEXT),
            TextNode("link", TextNode.LINK, "https://boot.dev"),
        ], text_to_textnodes(text))

    def test_markdown_to_blocks(self):
        markdown = '''
This is **bolded** paragraph

   This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line


* This is a list
* with items   
'''

        self.assertEqual([
            'This is **bolded** paragraph',
            'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line',
            '* This is a list\n* with items',
        ], markdown_to_blocks(markdown))


    def test_markdown_to_html(self):
        markdown = '''
### This is a level 3 heading

This is **bolded** paragraph

   This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line


* This is a list
* with items   
'''

        self.assertEqual(
            '<div><h3>This is a level 3 heading</h3><p>This is <b>bolded</b> paragraph</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here\nThis is the same paragraph on a new line</p><ul><li>This is a list</li><li>with items</li></ul></div>',
            markdown_to_html_node(markdown).to_html()
        )

    def test_extract_title(self):
        self.assertEqual([
            extract_title('# Hello'),
            extract_title('# Heading with **bolded** word'),
            extract_title('''
## Before lvl 1 heading

# Heading

### After lvl 1 heading
''')
        ], [
            'Hello',
            'Heading with <b>bolded</b> word',
            'Heading'
        ])


    def test_extract_title_invalid(self):
        self.assertRaises(Exception, lambda: extract_title('## Markdown **without** lvl 1 heading'))


if __name__ == "__main__":
    unittest.main()

