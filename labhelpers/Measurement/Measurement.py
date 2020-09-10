import numpy as np


class Measurement:
    @staticmethod
    def measure_n(n, func):
        vals = np.zeros(n)
        for i in range(n):
            vals[n] = func()
        return vals.mean(), vals.std(ddof=1)
