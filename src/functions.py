import os
import re

from pathlib import Path

from textnode import TextNode
from leafnode import LeafNode
from htmlnode import HTMLNode
from parentnode import ParentNode
from blocktype import (BlockType, block_to_block_type)
from filesystem import (get_file_contents, put_file_contents, map_dir)


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
        if node.text_type != TextNode.TEXT or delimiter not in node.text:
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
    return re.findall(r"(?:^|[^!])\[(.*?)\]\((.*?)\)", text)


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
        split_nodes_image,
        split_nodes_link,
        lambda nodes: split_nodes_delimiter(nodes, '**', TextNode.BOLD),
        lambda nodes: split_nodes_delimiter(nodes, '_', TextNode.ITALIC),
        lambda nodes: split_nodes_delimiter(nodes, '`', TextNode.CODE),
    ]

    nodes = [TextNode(text, TextNode.TEXT)]

    for transformer in transformers:
        nodes = transformer(nodes)

    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = re.split('\n{2,}', markdown.strip())

    return list(map(lambda block: block.strip(), blocks))


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = list(map(__block_to_html_node, blocks))

    return ParentNode('div', nodes)


def extract_title(markdown: str) -> str:
    for block in markdown_to_blocks(markdown):
        if 1 == BlockType.get_heading_size(block):
            return __heading_block_to_html_node(block).get_inner_html()
    
    raise Exception('Markdown does not contain any level 1 headings.')


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str = '/'):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    markdown = get_file_contents(from_path)
    template = get_file_contents(template_path)

    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    html = template.replace('{{ Title }}', title).replace('{{ Content }}', content)

    if '/' != basepath:
        html = html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    put_file_contents(dest_path, html)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str = '/'):
    def map_file(src_path: str, target_dir: str):
        target_path = os.path.join(target_dir, Path(src_path).with_suffix('.html').name)

        generate_page(src_path, template_path, target_path, basepath)

    map_dir(dir_path_content, dest_dir_path, map_file)


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


def __block_to_html_node(block: str) -> HTMLNode:
    type = block_to_block_type(block)

    if BlockType.QUOTE == type:
        return __quote_block_to_html_node(block)
    if BlockType.UNORDERED_LIST == type:
        return __unordered_list_block_to_html_node(block)
    if BlockType.ORDERED_LIST == type:
        return __ordered_list_block_to_html_node(block)
    if BlockType.CODE == type:
        return __code_block_to_html_node(block)
    if BlockType.HEADING == type:
        return __heading_block_to_html_node(block)
    
    return __paragraph_block_to_html_node(block)


def __quote_block_to_html_node(block: str) -> ParentNode:
    html_nodes = []

    for line in block.splitlines():
        text = line[1:].strip()
        text_nodes = text_to_textnodes(text)
        html_nodes.extend(map(text_node_to_html_node, text_nodes))

    return ParentNode('blockquote', html_nodes)


def __unordered_list_block_to_html_node(block: str) -> ParentNode:
    items = []

    for line in block.splitlines():
        text = line[1:].strip()
        html_nodes = __text_to_html_nodes(text)
        items.append(ParentNode('li', html_nodes))

    return ParentNode('ul', items)


def __ordered_list_block_to_html_node(block: str) -> ParentNode:
    items = []

    ordinal = 0
    for line in block.splitlines():
        ordinal += 1
        match = re.search(f'^{ordinal}\\.\\s+(?P<text>.*)$', line)
        html_nodes = __text_to_html_nodes(match.group('text'))
        items.append(ParentNode('li', html_nodes))

    return ParentNode('ol', items)


def __code_block_to_html_node(block: str) -> ParentNode:
    lines = block.splitlines()

    if (1 == len(lines)):
        text = block[3:-4]
    else:
        text = '\n'.join(lines[1:-1])

    return ParentNode('pre', [LeafNode('code', text)])


def __heading_block_to_html_node(block: str) -> ParentNode:
    match = re.search('^(?P<level>#{1,6})\\s+(?P<text>.*)$', block)
    level = len(match.group('level'))
    html_nodes = __text_to_html_nodes(match.group('text'))

    return ParentNode(f'h{level}', html_nodes)


def __paragraph_block_to_html_node(block: str) -> ParentNode:
    html_nodes = __text_to_html_nodes(block)

    return ParentNode('p', html_nodes)


def __text_to_html_nodes(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)

    return list(map(text_node_to_html_node, text_nodes))
