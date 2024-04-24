from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        if None == tag:
            raise ValueError('ParentNode must have a tag')

        if type(children) != list:
            raise ValueError('children must be a list')

        if 0 >= len(children):
            raise ValueError('children must not be empty')

        super().__init__(tag, None, children, props)

    def to_html(self):
        props = self.props_to_html()
        opening_tag = f'{self.tag} {props}'.strip()

        text = ''.join(map(
            lambda node: node.to_html(),
            self.children
        ))

        return f'<{opening_tag}>{text}</{self.tag}>'
