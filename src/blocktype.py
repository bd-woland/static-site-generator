import re

class BlockType():
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

    def get_type(block: str) -> str:
        if BlockType.is_heading(block):
            return BlockType.HEADING

        if BlockType.is_code(block):
            return BlockType.CODE

        if BlockType.is_quote(block):
            return BlockType.QUOTE

        if BlockType.is_unordered_list(block):
            return BlockType.UNORDERED_LIST

        if BlockType.is_ordered_list(block):
            return BlockType.ORDERED_LIST

        return BlockType.PARAGRAPH

    def is_heading(block: str) -> bool:
        return None != BlockType.get_heading_size(block)

    def get_heading_size(block: str) -> None|int:
        match = re.search('^#{1,6} ', block)

        if None == match:
            return None

        return match.end() - 1

    def is_code(block: str) -> bool:
        return '```' == block[:3] and '```' == block[-3:]

    def is_quote(block: str) -> bool:
        for line in block.splitlines():
            if '>' != line[0]:
                return False

        return True

    def is_unordered_list(block: str) -> bool:
        delimiter = block[0]
        if '*' != delimiter and '-' != delimiter:
            return False

        for line in block.splitlines():
            if f'{delimiter} ' != line[:2]:
                return False

        return True

    def is_ordered_list(block: str) -> bool:
        ordinal = 0
        for line in block.splitlines():
            ordinal += 1
            if None == re.search(f'^{ordinal}\\. ', line):
                return False

        return True


def block_to_block_type(block: str) -> str:
    return BlockType.get_type(block)

