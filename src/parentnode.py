from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict|None = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if None == self.tag:
            raise ValueError('ParentNode must have a tag')

        attributes = self.props_to_html()
        opening_tag = f'{self.tag} {attributes}'.strip()

        inner_html = self.get_inner_html()

        return f'<{opening_tag}>{inner_html}</{self.tag}>'

    def get_inner_html(self) -> str:
        if type(self.children) != list:
            raise ValueError('children must be a list')

        if 0 >= len(self.children):
            raise ValueError('children must not be empty')

        return ''.join(map(
            lambda node: node.to_html(),
            self.children
        ))
