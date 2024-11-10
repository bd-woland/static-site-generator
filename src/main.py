from textnode import TextNode
from functions import (text_node_to_html_node)
from filesystem import (copy_dir)
import os

def main():
    copy_dir('static', 'public')

    text_node = TextNode('This is a text node', TextNode.LINK, 'https://www.boot.dev')

    print(text_node_to_html_node(text_node).to_html())


main()
