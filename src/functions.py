import re

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
    def split_node_delimiter(node: TextNode) -> list[TextNode]:
        if delimiter not in node.text:
            return [node]

        parts = node.text.split(delimiter)
        parts_len = len(parts)

        if 0 == parts_len % 2:
             raise Exception('Matching closing delimiter not found')
        
        split_node = []

        for i in range(parts_len):
            if '' == parts[i]:
                continue
            elif 0 == i % 2:
                split_node.append(TextNode(parts[i], TextNode.TEXT))
            else:
                split_node.append(TextNode(parts[i], text_type))

        return split_node

    return __split_text_nodes(old_nodes, split_node_delimiter)


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[(str, str)]:
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode|HTMLNode]) -> list[TextNode|HTMLNode]:
    def split_node_image(node: TextNode) -> list[TextNode]:
        images = extract_markdown_images(node.text)

        if 0 == len(images):
            return [node]

        return __extract_url_nodes(node, images, lambda image: f'![{image[0]}]({image[1]})', TextNode.IMAGE)

    return __split_text_nodes(old_nodes, split_node_image)


def split_nodes_link(old_nodes: list[TextNode|HTMLNode]) -> list[TextNode|HTMLNode]:
    def split_node_link(node: TextNode) -> list[TextNode]:
        links = extract_markdown_links(node.text)
 
        if 0 == len(links):
            return [node]

        return __extract_url_nodes(node, links, lambda link: f'[{link[0]}]({link[1]})', TextNode.LINK)

    return __split_text_nodes(old_nodes, split_node_link)


def text_to_textnodes(text: str) -> list[TextNode]:
    transformers = [
        lambda nodes: split_nodes_delimiter(nodes, '**', TextNode.BOLD),
        lambda nodes: split_nodes_delimiter(nodes, '*', TextNode.ITALIC),
        lambda nodes: split_nodes_delimiter(nodes, '`', TextNode.CODE),
        split_nodes_image,
        split_nodes_link
    ]

    nodes = [TextNode(text, TextNode.TEXT)]

    for transformer in transformers:
        nodes = transformer(nodes)

    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = re.split('\n{2,}', markdown)

    return list(map(lambda block: block.strip(), blocks))


def __split_text_nodes(old_nodes: list[TextNode|HTMLNode], node_splitter: callable) -> list[TextNode|HTMLNode]:
    split_nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode) or TextNode.TEXT != node.text_type:
            split_nodes.append(node)
        else:
            split_nodes.extend(node_splitter(node))

    return split_nodes


def __extract_url_nodes(node: TextNode, text_and_urls: list[tuple[str, str]], delimiter_factory: callable, text_type: str) -> list[TextNode]:
    split_node = []
    current_node_text = node.text

    for item in text_and_urls:
        delimiter = delimiter_factory(item)
        parts = current_node_text.split(delimiter, 1)

        if '' != parts[0]:
            split_node.append(TextNode(parts[0], TextNode.TEXT))

        split_node.append(TextNode(item[0], text_type, item[1]))

        current_node_text = parts[1]

    if '' != current_node_text:
        split_node.append(TextNode(current_node_text, node.text_type))

    return split_node

