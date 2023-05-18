

class Scheduler:
    def __init__(self, rate):
        self.__rate = rate
        self.step = 0

    def do_one_step(self):
        self.step += 1

    def calculate(self, val):
        pass