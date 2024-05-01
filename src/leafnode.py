from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str|None = None, value: str = '', props: dict|None = None):
        super().__init__(tag, value, props=props)

    def to_html(self) -> str:
        if None == self.value:
            raise ValueError('LeafNode must have a value')

        if None == self.tag:
            return self.value

        attributes = self.props_to_html()
        opening_tag = f'{self.tag} {attributes}'.strip()

        return f'<{opening_tag}>{self.value}</{self.tag}>'
