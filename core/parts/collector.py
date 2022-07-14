


class Collector:
    def __init__(self,core):
        self.core = core

    def collect(self):
        self.core.again = 'from imported module'
        self.core.test()

    def collectt(self):
        self.core.test()