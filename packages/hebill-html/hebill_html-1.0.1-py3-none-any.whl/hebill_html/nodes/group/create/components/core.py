class Components:
    def __init__(self, sir):
        self.senior = sir

    def alert(self, text):
        from .....components import Alert
        return Alert(self.senior, text)

    def table(self):
        from .....components import Table
        return Table(self.senior)
