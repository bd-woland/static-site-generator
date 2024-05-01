from textnode import TextNode
from leafnode import LeafNode
from htmlnode import HTMLNode


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


def split_nodes_delimiter(old_nodes: list[TextNode|HTMLNode], delimiter: str, text_type: str) -> list[TextNode|HTMLNode]:
    def split_node_delimiter(node: TextNode):
        parts = node.text.split(delimiter)
        parts_len = len(parts)

        if 0 == parts_len % 2:
             raise Exception('Matching closing delimiter not found')
        
        split_node = []

        for i in range(parts_len):
            if '' == parts[i]:
                continue
            elif 0 == i % 2:
                split_node.append(TextNode(parts[i], node.text_type))
            else:
                split_node.append(TextNode(parts[i], text_type))

        return split_node

    split_nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode) or delimiter not in node.text:
            split_nodes.append(node)
        else:
            split_nodes.extend(split_node_delimiter(node))

    return split_nodes
