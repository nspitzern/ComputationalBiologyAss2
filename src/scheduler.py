class Scheduler:
    def __init__(self, init_val: float, decay: float, min_val: float = 0.1):
        self.__decay = decay
        self.__init_val = init_val
        self.__min_val = min_val

    @property
    def min_val(self) -> float:
        return self.__min_val

    @property
    def decay(self) -> float:
        return self.__decay

    def calculate(self, step: int) -> float:
        # percent = self.__init_val
        # if history.last_n_best_change(20) < 0.05:
        #     percent = min(percent * 3, 1)
        # return percent
        return max(self.__init_val / (1 + self.__decay * step), self.__min_val)
