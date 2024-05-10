from ...nodes import Tag


class Div(Tag):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'div')
        self.add_junior(text)
