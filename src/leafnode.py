from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = '', props = None):
        if None == value:
            raise ValueError('LeafNode must have a value')

        super().__init__(tag, value, props=props)

    def to_html(self):
        if None == self.tag:
            return self.value
        
        props = self.props_to_html()
        opening_tag = f'{self.tag} {props}'.strip()

        return f'<{opening_tag}>{self.value}</{self.tag}>'
