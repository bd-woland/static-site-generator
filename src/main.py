from textnode import TextNode
from leafnode import LeafNode


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if TextNode.TEXT == text_node.text_type:
        return LeafNode(value=text_node.text)
    if TextNode.BOLD == text_node.text_type:
        return LeafNode('b', text_node.text)
    if TextNode.ITALIC == text_node.text_type:
        return LeafNode('i', text_node.text)
    if TextNode.CODE == text_node.text_type:
        return LeafNode('code', text_node.text)
    if TextNode.LINK == text_node.text_type:
        return LeafNode('a', text_node.text, {'href': text_node.url})
    if TextNode.IMAGE == text_node.text_type:
        return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
    raise ValueError('Unsupported TextNode type')


def main():
    text_node = TextNode('This is a text node', TextNode.LINK, 'https://www.boot.dev')

    print(text_node_to_html_node(text_node).to_html())


main()
