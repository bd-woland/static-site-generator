import unittest

from blocktype import (BlockType, block_to_block_type)


class TestHTMLNode(unittest.TestCase):
    def test_block_to_block_type(self):
        test_cases = {
            BlockType.HEADING: [
                '# H1',
                '## H2',
                '### H3',
                '#### H4',
                '##### H5',
                '###### H6',
            ],
            BlockType.CODE: [
                '```single_line_code_block = None```',
                '''```json
{"key": [1, 2,3]}
```''',
            ],
            BlockType.QUOTE: [
                '''>single line quote block''',
                '''> multi
>line
> quote
>block''',
            ],
            BlockType.UNORDERED_LIST: [
                '''* asterisks
* delimited
* list''',
                '''- dash
- delimited
- list''',
            ],
            BlockType.ORDERED_LIST: [
                '''1. ordered
2. list
3. but
4. I
5. actually
6. need
7. at
8. least
9. 10
10. items
''',
            ],
            BlockType.PARAGRAPH: [
                'single line paragraph',
                'multi\nline\nparagraph',
                '####### fake heading',
                '```not really a code block``',
                '>quote block\nbut not quite',
                '* listing\n* elements\n*is hard',
                '''- mixed\n* delimited lists\n- are invalid''',
                '1. I cannot\n2. count to\n10. ten',
                '1. Punctuation\n2, is\n3. hard',
            ],
        }

        for block_type, blocks in test_cases.items():
            for block in blocks:
                self.assertEqual(block_type, block_to_block_type(block))


if __name__ == "__main__":
    unittest.main()

