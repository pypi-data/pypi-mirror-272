from ...nodes import Tag


class Span(Tag):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'span')
        self.output_break_inner = False
        self.add_junior(text)
