import numpy as np


class Measurement:
    @staticmethod
    def measure_n(n: int, func):
        if type(n) != int:
            raise TypeError("Number of measurements must be integer value.")
        if n < 1:
            raise ValueError("Number of measurements must be 1 or larger.")
        if n == 1:
            return func()
        else:
            vals = np.zeros(n)
            for i in range(n):
                vals[n] = func()
            return vals.mean(), vals.std(ddof=1)
