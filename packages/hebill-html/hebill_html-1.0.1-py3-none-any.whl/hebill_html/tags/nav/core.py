from ...nodes import Tag


class Nav(Tag):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'nav')
        self.add_junior(text)
