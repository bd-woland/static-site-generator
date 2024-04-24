class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if None == self.props:
            return ''

        return ' '.join(map(
            lambda prop: f'{prop[0]}="{prop[1]}"',
            self.props.items()
        ))

    def __repr__(self):
        return f'{self.__class__}({self.tag}, {self.value}, {self.props}, {self.children})'
